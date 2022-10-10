# from _future_ import absolute_import
# from _future_ import unicode_literals
from __future__ import absolute_import
from __future__ import unicode_literals
import os

from django.conf import settings

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")

app = Celery("django_project")
app.conf.enable_utc = False

app.conf.update(timezone="Asia/Kolkata")

app.config_from_object(settings, namespace="CELERY")

# Celery Beat Settings
app.conf.beat_schedule = {
    "send-mail-every-day-at-8": {
        "task": "django_application.tasks.send_email_task",
        "schedule": crontab(minute=1),
        #'args': (2,)
    }
}

# Celery Schedules - https://docs.celeryproject.org/en/stable/reference/celery.schedules.html

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")

