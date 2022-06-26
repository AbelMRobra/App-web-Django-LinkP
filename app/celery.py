import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

from django.conf import settings

app = Celery('app')
app.config_from_object('django.conf:app', namespace='CELERY')
app.autodiscover_tasks(settings.INSTALLED_APPS)
app.conf.update(
    BROKER_URL = 'redis://redis:6379/0',
    CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
)




