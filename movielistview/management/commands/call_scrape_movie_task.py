from django.core.management.base import BaseCommand, CommandError
from ...tasks import scrape_movies_task

class Command(BaseCommand):
    

    def handle(self, *args, **options):
        scrape_movies_task.run()