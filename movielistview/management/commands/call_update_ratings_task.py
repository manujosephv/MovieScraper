from django.core.management.base import BaseCommand, CommandError
from ...tasks import update_ratings_task

class Command(BaseCommand):
    

    def handle(self, *args, **options):
        update_ratings_task.run()