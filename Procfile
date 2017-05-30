web: gunicorn MovieScraper.wsgi
main_worker: celery -A MovieScraper  --beat --loglevel=info