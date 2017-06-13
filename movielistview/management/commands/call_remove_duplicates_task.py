from django.core.management.base import BaseCommand, CommandError
from ...tasks import remove_duplicates_task

class Command(BaseCommand):
    

    def handle(self, *args, **options):
        remove_duplicates_task.run()