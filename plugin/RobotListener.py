import json
from datetime import datetime
from settings import ROBOT_REDIS_URL, CASE_RESULT_KEY_PREFIX, REDIS_EXPIRE_TIME
from handler.redisclient import RedisClient


class RobotListener(object):
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self, task_id):
        self.task_id = task_id
        self.conn = RedisClient(ROBOT_REDIS_URL).connector
        self.case_redis_key = CASE_RESULT_KEY_PREFIX + self.task_id

    def start_suite(self, data, result):
        pass

    def start_test(self, data, result):
        pass

    def end_test(self, data, result):
        date_format = "%Y%m%d %H:%M:%S.%f"
        start_time = datetime.strptime(result.starttime, date_format).timestamp()
        end_time = datetime.strptime(result.endtime, date_format).timestamp()
        value = {'start_time': start_time, 'end_time': end_time, 'result': result.status}
        json_value = json.dumps(value)
        self.conn.hset(self.case_redis_key, data.doc, json_value)
        self.conn.expire(self.case_redis_key, REDIS_EXPIRE_TIME)

    def end_suite(self, data, result):
        pass

    def close(self):
        pass
