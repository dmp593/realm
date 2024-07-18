import os
import requests
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
def load_env(env_filepath):
    if os.path.exists(env_filepath):
        load_dotenv(env_filepath)

def get_long_lived_user_token(short_lived_token, app_id, app_secret):
    url = f"https://graph.facebook.com/v20.0/oauth/access_token"
    params = {
        'grant_type': 'fb_exchange_token',
        'client_id': app_id,
        'client_secret': app_secret,
        'fb_exchange_token': short_lived_token,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data['access_token'], datetime.now() + timedelta(days=60)

def get_page_access_token(user_access_token, page_id):
    url = f"https://graph.facebook.com/v20.0/{page_id}"
    params = {
        'fields': 'access_token',
        'access_token': user_access_token,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data['access_token']

def set_env_vars(env_filepath, vars_dict):
    env_vars = vars_dict.copy()
    if os.path.exists(env_filepath):
        with open(env_filepath, 'r') as file:
            lines = file.readlines()
        for line in lines:
            key, _, value = line.partition('=')
            if key.strip() not in env_vars:
                env_vars[key.strip()] = value.strip()
    with open(env_filepath, 'w') as file:
        for key, value in env_vars.items():
            file.write(f'{key}={value}\n')
            os.environ[key] = value
    for key, value in vars_dict.items():
        print(f"Set {key} to {value}")

def refresh_long_lived_token(long_lived_user_token, app_id, app_secret):
    url = f"https://graph.facebook.com/v20.0/oauth/access_token"
    params = {
        'grant_type': 'fb_exchange_token',
        'client_id': app_id,
        'client_secret': app_secret,
        'fb_exchange_token': long_lived_user_token,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data['access_token'], datetime.now() + timedelta(days=60)

def main():
    if len(sys.argv) < 2:
        print("Usage: python token_refresh.py <SHORT_LIVED_TOKEN> [<ENV_FILE_PATH>]")
        sys.exit(1)
    
    short_lived_token = sys.argv[1]
    env_filepath = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(__file__), '.facebook')

    # Load existing environment variables from file
    load_env(env_filepath)

    # Load environment variables or set defaults
    FACEBOOK_APP_ID = os.getenv('FACEBOOK_APP_ID')
    FACEBOOK_APP_SECRET = os.getenv('FACEBOOK_APP_SECRET')
    FACEBOOK_PAGE_ID = os.getenv('FACEBOOK_PAGE_ID')
    LONG_LIVED_USER_TOKEN = os.getenv('FACEBOOK_USER_LONG_LIVED_TOKEN')
    USER_TOKEN_EXPIRY = os.getenv('FACEBOOK_USER_TOKEN_EXPIRY')

    try:
        if LONG_LIVED_USER_TOKEN and USER_TOKEN_EXPIRY:
            expiry_date = datetime.strptime(USER_TOKEN_EXPIRY, '%Y-%m-%d %H:%M:%S')
            if expiry_date > datetime.now():
                print("Refreshing long-lived user token.")
                long_lived_user_token, user_token_expiry = refresh_long_lived_token(LONG_LIVED_USER_TOKEN, FACEBOOK_APP_ID, FACEBOOK_APP_SECRET)
                set_env_vars(env_filepath, {
                    'FACEBOOK_USER_LONG_LIVED_TOKEN': long_lived_user_token,
                    'FACEBOOK_USER_TOKEN_EXPIRY': user_token_expiry.strftime('%Y-%m-%d %H:%M:%S'),
                    'FACEBOOK_APP_ID': FACEBOOK_APP_ID,
                    'FACEBOOK_APP_SECRET': FACEBOOK_APP_SECRET,
                    'FACEBOOK_PAGE_ID': FACEBOOK_PAGE_ID
                })
            else:
                print("Long-lived user token has expired, refreshing using short-lived token.")
                long_lived_user_token, user_token_expiry = get_long_lived_user_token(short_lived_token, FACEBOOK_APP_ID, FACEBOOK_APP_SECRET)
                set_env_vars(env_filepath, {
                    'FACEBOOK_USER_LONG_LIVED_TOKEN': long_lived_user_token,
                    'FACEBOOK_USER_TOKEN_EXPIRY': user_token_expiry.strftime('%Y-%m-%d %H:%M:%S'),
                    'FACEBOOK_APP_ID': FACEBOOK_APP_ID,
                    'FACEBOOK_APP_SECRET': FACEBOOK_APP_SECRET,
                    'FACEBOOK_PAGE_ID': FACEBOOK_PAGE_ID
                })
        else:
            print("No long-lived user token found, refreshing using short-lived token.")
            long_lived_user_token, user_token_expiry = get_long_lived_user_token(short_lived_token, FACEBOOK_APP_ID, FACEBOOK_APP_SECRET)
            set_env_vars(env_filepath, {
                'FACEBOOK_USER_LONG_LIVED_TOKEN': long_lived_user_token,
                'FACEBOOK_USER_TOKEN_EXPIRY': user_token_expiry.strftime('%Y-%m-%d %H:%M:%S'),
                'FACEBOOK_APP_ID': FACEBOOK_APP_ID,
                'FACEBOOK_APP_SECRET': FACEBOOK_APP_SECRET,
                'FACEBOOK_PAGE_ID': FACEBOOK_PAGE_ID
            })

        page_access_token = get_page_access_token(long_lived_user_token, FACEBOOK_PAGE_ID)
        set_env_vars(env_filepath, {'FACEBOOK_PAGE_ACCESS_TOKEN': page_access_token})

        print("Tokens updated successfully.")
    except Exception as e:
        print(f"Error during token refresh: {e}")

if __name__ == "__main__":
    main()
