from django.core.management.base import BaseCommand, CommandError
from ...tasks import update_release_type

class Command(BaseCommand):
    

    def handle(self, *args, **options):
        update_release_type.run()