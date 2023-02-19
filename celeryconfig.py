from kombu import Queue
from settings import REDIS_HOST, REDIS_PORT


# Celery config
imports = ('task.tasks',)
broker_url = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
result_backend = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
task_queues = (
    Queue('runner', routing_key='runner'),
 )
task_routes = {
    'task.robot.robot_runner': {'queue': 'runner', 'routing_key': 'runner'}
 }
# notify mq message is consumed only task finish
ack_late = True
# data type of task accept
accept_content = ['json']
# serialize type
task_serializer = 'json'
# timezone
timezone = 'Asia/Shanghai'
enable_utc = False
# task result expire time(s)
result_expires = 60*60
# not receive ack will send to other worker
disable_rate_limits = True
# result not send to broker
# ignore_result = True
# disable prefetch task, default 4
worker_prefetch_multiplier = 1
# worker concurrency num
worker_concurrency = 2
# max execute task num will die
worker_max_tasks_per_child = 1000

