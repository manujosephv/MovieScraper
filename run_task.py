#!/usr/bin/env python
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MovieScraper.settings")
from movielistview.tasks import delete_read_movies_task

print "in run task"
delete_read_movies_task.run()