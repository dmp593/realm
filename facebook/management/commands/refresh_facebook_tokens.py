from django.core.management.base import BaseCommand
from facebook.utils import get_token, refresh_facebook_tokens


class Command(BaseCommand):
    help = 'Refresh Facebook tokens and update settings'

    def handle(self, *args, **options):
        user_long_lived_token = get_token('user-long-lived')

        if not user_long_lived_token:
            user_short_lived_token = get_token('user-short-lived')
            if not user_short_lived_token:
                self.stdout.write(self.style.ERROR('Required short-lived user token is missing.'))
                return

        tokens = refresh_facebook_tokens()
        if not tokens:
            self.stdout.write(self.style.ERROR('Failed to refresh Facebook tokens.'))
            return

        user_access_token, page_access_token = tokens

        if not user_access_token:
            self.stdout.write(self.style.ERROR('Failed to refresh the long-lived user access token.'))
            return

        if not page_access_token:
            self.stdout.write(self.style.ERROR('Failed to refresh the page access token.'))
            return

        self.stdout.write(self.style.SUCCESS("Facebook tokens updated successfully."))
