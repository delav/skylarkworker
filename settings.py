from pathlib import Path

# Project base dir
BASE_DIR = Path(__file__).resolve().parent
# run file path
FILE_DIR = BASE_DIR / 'files'

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
)
RUNNER_QUEUE = 'runner'
RUNNER_TASK = 'task.robot.tasks.robot_runner'
RUNNER_ROUTING_KEY = 'robot.runner'
NOTIFIER_QUEUE = 'notifier'
NOTIFIER_TASK = 'task.robot.tasks.robot_notifier'
NOTIFIER_ROUTING_KEY = 'robot.notifier'


