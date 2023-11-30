import os
import sys
from celery import Celery

WORKER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, WORKER)

os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
app = Celery('skylarkworker')
app.config_from_object('celeryconfig')
