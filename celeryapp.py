import os
from celery import Celery

# resolve "Task handler raised error: ValueError('not enough values to unpack (expected 3, got 0)')" error
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
app = Celery('skylarkworker')
app.config_from_object('celeryconfig')
