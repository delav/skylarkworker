import os
from celery import Celery
from celery.signals import heartbeat_sent, worker_ready, worker_shutdown
from settings import IP, HOSTNAME, EXCHANGE_QUEUE, EXCLUSIVE_QUEUE, HEARTBEAT_TASK, COLLECT_TASK

os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
app = Celery('skylarkworker')
app.config_from_object('celeryconfig')


# @heartbeat_sent.connect
# def send_heartbeat(**kwargs):
#     app.send_task(
#         HEARTBEAT_TASK,
#         queue=EXCHANGE_QUEUE,
#         args=(IP, )
#     )


@worker_ready.connect
def on_worker_read(**kwargs):
    worker_info = {
        'ip': IP,
        'hostname': HOSTNAME,
        'queue': EXCLUSIVE_QUEUE
    }
    app.send_task(
        COLLECT_TASK,
        queue=EXCHANGE_QUEUE,
        args=('ready', worker_info)
    )


@worker_shutdown.connect
def on_worker_shutdown(**kwargs):
    worker_info = {
        'ip': IP,
        'hostname': HOSTNAME,
        'queue': EXCLUSIVE_QUEUE
    }
    app.send_task(
        COLLECT_TASK,
        queue=EXCHANGE_QUEUE,
        args=('shutdown', worker_info)
    )
