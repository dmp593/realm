from os import getenv
from dotenv import load_dotenv
from django.conf import settings


def load_facebook_env():
	facebook_env_file = settings.BASE_DIR.joinpath('facebook').joinpath('.facebook')
	load_dotenv(facebook_env_file)


def get_facebook_page_id() -> str:
	load_facebook_env()
	return getenv('FACEBOOK_PAGE_ID', '')


def get_facebook_page_access_token() -> str:
	load_facebook_env()
	return getenv('FACEBOOK_PAGE_ACCESS_TOKEN', '')
