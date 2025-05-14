import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Blogger.settings')

app = Celery('Blogger')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

import Blog.utils