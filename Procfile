web: gunicorn MovieScraper.wsgi
main_worker: celery -A MovieScraper worker -l info
beat: celery -A MovieScraper beat 