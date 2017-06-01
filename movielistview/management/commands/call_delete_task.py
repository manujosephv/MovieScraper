from django.core.management.base import BaseCommand, CommandError
from ...tasks import delete_read_movies_task

class Command(BaseCommand):
    

    def handle(self, *args, **options):
        delete_read_movies_task.run()