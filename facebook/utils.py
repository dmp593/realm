from environ import re
import requests

from datetime import datetime, timedelta
from django.conf import settings
from django.utils.timezone import now
from facebook.models import FacebookAccessToken


def get_facebook_app_id():
    return settings.FACEBOOK_APP_ID


def get_token(scope: str) -> str | None:
    queryset = FacebookAccessToken.objects.filter(scope=scope, expiry__gt=now())

    if not queryset.exists():
        return None

    return queryset.first().access_token


def set_token(scope, access_token, expiry) -> str:
    FacebookAccessToken.objects.update_or_create(
        scope=scope,
        defaults={'access_token': access_token, 'expiry': expiry}
    )

    return access_token


def refresh_user_access_token(exchange_token: str):
    url = f"https://graph.facebook.com/v20.0/oauth/access_token"
    params = {
        'grant_type': 'fb_exchange_token',
        'client_id': settings.FACEBOOK_APP_ID,
        'client_secret': settings.FACEBOOK_APP_SECRET,
        'fb_exchange_token': exchange_token,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    
    data = response.json()
    expiry = now() + timedelta(days=60)
    
    return set_token('user-long-lived', data['access_token'], expiry)


def get_user_id(user_access_token: str):
    url = "https://graph.facebook.com/me"
    params = {
        'access_token': user_access_token,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    
    data = response.json()
    return data['id']


def refresh_page_access_token(user_access_token: str):
    user_id = get_user_id(user_access_token)
    
    url = f"https://graph.facebook.com/{user_id}/accounts"
    params = {
        'access_token': user_access_token,
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    data = response.json()
    
    if 'data' in data:
        for page in data['data']:
            if 'access_token' in page and 'id' in page and page['id'] == settings.FACEBOOK_PAGE_ID:
                expiry = now() + timedelta(hours=1)  # Assuming page token expiry 1h
                return set_token('page', page['access_token'], expiry)
    
    return None


def refresh_facebook_tokens() -> tuple[str | None, str | None]:
    user_access_token = get_token('user-long-lived') or get_token('user-short-lived')

    if user_access_token:
        user_access_token = refresh_user_access_token(exchange_token=user_access_token)
        page_access_token = refresh_page_access_token(user_access_token)

        return user_access_token, page_access_token

    return None, None
