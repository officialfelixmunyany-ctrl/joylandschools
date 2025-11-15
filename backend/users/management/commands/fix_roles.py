from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):
    help = 'Fix user roles: set superusers to system_admin and optionally fix users with incorrect roles.'

    def add_arguments(self, parser):
        parser.add_argument('--fix-superusers', action='store_true', help='Ensure all superusers have role system_admin')

    def handle(self, *args, **options):
        if options['fix_superusers']:
            supers = User.objects.filter(is_superuser=True).exclude(role='system_admin')
            count = supers.count()
            for u in supers:
                u.role = 'system_admin'
                u.save()
                self.stdout.write(self.style.SUCCESS(f'Set role=system_admin for {u.username}'))
            if count == 0:
                self.stdout.write('No superusers needed changes.')
        else:
            self.stdout.write('No action taken. Use --fix-superusers to correct superuser roles.')
