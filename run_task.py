#!/usr/bin/env python
from movielistview.tasks import delete_read_movies_task

print "in run task"
delete_read_movies_task.run()