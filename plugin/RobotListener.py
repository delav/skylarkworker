from settings import ROBOT_REDIS_URL, CASE_RESULT_KEY_PREFIX
from handler.redisclient import RedisClient


class RobotListener(object):
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self, build_id):
        self.build_id = build_id
        self.conn = RedisClient(ROBOT_REDIS_URL).connector
        self.case_redis_key = CASE_RESULT_KEY_PREFIX + self.build_id

    def start_suite(self, data, result):
        pass

    def start_test(self, data, result):
        pass

    def end_test(self, data, result):
        self.conn.hset(self.case_redis_key, data.doc, result.status)

    def end_suite(self, data, result):
        pass

    def close(self):
        pass
