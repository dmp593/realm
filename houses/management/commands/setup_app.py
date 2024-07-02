from django.conf import settings

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Initialize the application by running migrations, loading initial data, and creating a superuser.'

    def add_arguments(self, parser):
        parser.add_argument(
            '-u',
            '--username',
            type=str,
            default='alcinaroque',
            help='Username for the superuser (default: alcinaroque)'
        )
        
        parser.add_argument(
            '-e',
            '--email',
            type=str,
            default='alcinaroque@alcinaroque.pt',
            help='Email address for the superuser (default: alcinaroque@alcinaroque.pt)'
        )
        
        parser.add_argument(
            '-p',
            '--password',
            type=str,
            required=not settings.DEBUG,
            default='secret',
            help='Password for the superuser'
        )
        
        parser.add_argument(
            '-n',
            '--first-name',
            type=str,
            default='Alcina',
            help='First name for the superuser (default: Alcina)'
        )
        
        parser.add_argument(
            '-s',
            '--last-name',
            type=str,
            default='Roque',
            help='Last name for the superuser (default: Roque)'
        )

    def handle(self, *args, **kwargs):
        # Handle user arguments with defaults
        username = kwargs.get('username')
        password = kwargs.get('password')
        
        email = kwargs.get('email')
        
        first_name = kwargs.get('first_name')
        last_name = kwargs.get('last_name')

        # Call migrate command
        self.stdout.write(self.style.NOTICE('Running migrate...'))
        
        try:
            call_command('migrate')
        except CommandError as e:
            raise CommandError(f'Error running migrate command: {str(e)}') from e

        # Call loaddata commands
        self.stdout.write(self.style.NOTICE('Loading initial data...'))
        try:
            call_command('loaddata', 'houses/countries')
            call_command('loaddata', 'houses/districts')
            call_command('loaddata', 'houses/municipalities')
            call_command('loaddata', 'houses/parishes')
            call_command('loaddata', 'houses/locales')
            call_command('loaddata', 'houses/conditions')
            call_command('loaddata', 'houses/types')
            call_command('loaddata', 'houses/typologies')
            call_command('loaddata', 'houses/energies-certificates')
        except CommandError as e:
            raise CommandError(f'Error loading initial data: {str(e)}') from e

        # Create superuser
        self.stdout.write(self.style.NOTICE('Creating superuser...'))
        try:
            User.objects.create_superuser(username, email, password, first_name=first_name, last_name=last_name)
        except Exception as e:
            raise CommandError(f'Error creating superuser: {str(e)}') from e

        # Final success message
        self.stdout.write(
            self.style.SUCCESS(
                'Initialization completed successfully. '
                'Migrations applied, initial data loaded, and superuser created.'
            )
        )
