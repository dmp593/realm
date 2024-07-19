from environ import re
import requests

from django.conf import settings
from django.db.models import Q

from django.utils.timezone import now
from datetime import datetime, timedelta

from facebook.models import FacebookAccessToken


def get_facebook_app_id():
    return settings.FACEBOOK_APP_ID


def get_token(scope: str) -> str | None:
    where = Q(scope=scope) & ( Q(expiry__gt=now()) | Q(expiry__isnull=True) )
    queryset = FacebookAccessToken.objects.filter(where)

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
    expiry = now() + timedelta(seconds=data.get('expires_in', 3600))
    
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
                return set_token('page', page['access_token'], expiry=None)
    
    return None


def refresh_facebook_tokens() -> tuple[str | None, str | None]:
    #  a long lived user access token has an expiry of 60 days...
    user_access_token = get_token('user-long-lived') or get_token('user-short-lived')

    if user_access_token:
        user_access_token = refresh_user_access_token(exchange_token=user_access_token)
    
    # https://developers.facebook.com/docs/facebook-login/guides/access-tokens/get-long-lived/
    # according to fb documentation, page access token never expires...
    page_access_token = get_token('page')

    if not page_access_token:
        page_access_token = refresh_page_access_token(user_access_token) if user_access_token else None

    return user_access_token, page_access_token

