import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djouman.settings.local")
app = Celery("djouman")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
