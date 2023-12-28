import socket
from pathlib import Path

# get local hostname and ip addr
HOSTNAME = socket.gethostname()
IP = socket.gethostbyname(HOSTNAME)

# Project base dir
BASE_DIR = Path(__file__).resolve().parent
# run file path
FILE_DIR = BASE_DIR / 'files'

# Library path
LIBRARY_GIT = 'https://github.com/delav/skylarklibrary.git'
LIBRARY_PATH = BASE_DIR.parent

# Redis
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379

# Run case result db
REDIS_EXPIRE_TIME = 60*60*24*1
ROBOT_REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/1'
CASE_RESULT_KEY_PREFIX = 'robot:case:'
TASK_RESULT_KEY_PREFIX = 'robot:task:'

# Celery task
CELERY_TASKS_PATH = (
    'task.robot.tasks',
    'task.exchange.tasks'
)

RUNNER_QUEUE = 'runner'
NOTIFIER_QUEUE = 'notifier'
EXCHANGE_QUEUE = 'exchanger'
EXCLUSIVE_QUEUE = 'worker_' + IP
NOTIFIER_TASK = 'task.robot.tasks.robot_notifier'
RUNNER_TASK = 'task.robot.tasks.robot_runner'
HEARTBEAT_TASK = 'task.exchange.tasks.heartbeat'
COLLECT_TASK = 'task.exchange.tasks.worker_collector'
COMMAND_TASK = 'task.exchange.tasks.command_executor'



