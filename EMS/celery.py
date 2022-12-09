from __future__ import absolute_import, unicode_literals

import os
from time import timezone
from celery import Celery


from django.conf import settings
from celery.schedules import crontab 

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EMS.settings')

app = Celery('EMS')
app.conf.enable_utc = False

app.conf.update(timezone = 'Asia/Kolkata ')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object(settings, namespace='CELERY')


# Celery beat settings

app.conf.beat_schedule = {
    'email' : {
        'task' : 'application.tasks.email_Job',
        'schedule' : crontab(minute=24, hour=11),
        #'args' : (), 
    }
}

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

