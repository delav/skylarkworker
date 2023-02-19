# Redis
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379

# Run case result db
ROBOT_REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/1'
CASE_RESULT_KEY_PREFIX = 'robot:case:'
TASK_RESULT_KEY_PREFIX = 'robot:task:'


