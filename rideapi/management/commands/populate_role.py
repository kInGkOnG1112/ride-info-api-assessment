import time

from django.core.management.base import BaseCommand
from app_main.models import Role


class Command(BaseCommand):
    def handle(self, *args, **options):
        start = time.time()
        default_role_list = [
            {
                'name': 'Admin',
                'code': 'R001',
            },
            {
                'name': 'Driver',
                'code': 'R002',
            },
            {
                'name': 'Rider',
                'code': 'R003',
            }
        ]
        for role in default_role_list:
            role_obj, is_created = Role.objects.get_or_create(code=role['code'])
            role_obj.name = role['name']
            role_obj.save()

        end = time.time()
        self.stdout.write(self.style.SUCCESS('%f seconds' % (end - start)))
        self.stdout.write(self.style.SUCCESS('Successfully populated default roles'))

