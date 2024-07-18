from typing import Any

from django.conf import settings


def get_setting(key: str, or_default: str = '') -> Any:
    return getattr(settings, key, or_default)


def get_facebook_page_id(or_default: str = '') -> str:
    return get_setting('FACEBOOK_PAGE_ID', or_default)


def get_facebook_page_access_token(or_default: str = '') -> str:
    return get_setting('FACEBOOK_PAGE_ACCESS_TOKEN', or_default)