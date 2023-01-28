from datetime import datetime
from settings import ROBOT_REDIS_URL, CASE_RESULT_KEY_PREFIX
from utils.redisclient import RedisClient
from utils.resultreader import suite_result_handler
from celeryapp import app


class RobotListener(object):
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self, build_id):
        self.build_id = build_id
        self.conn = RedisClient(ROBOT_REDIS_URL).connector
        self.case_redis_key = CASE_RESULT_KEY_PREFIX + self.build_id

    def start_suite(self, data, result):
        # print("suite data: %s" % data)
        # print("Start suite: %s" % data.suites)
        # print("suite cases: %s" % data.tests)
        # print("suite_test_count: %s" % data.test_count)
        pass

    def start_test(self, data, result):
        # print("start test data: {}".format(dir(data)))
        # print("start test result: {}".format(dir(result)))
        # print("start test name:{}".format(data.name))
        # print("CaseID:{}".format(data.doc))
        pass

    def end_test(self, data, result):
        # print("end test data: {}".format(dir(data)))
        # print("end test result: {}".format(dir(result)))
        # print("test result:{}".format(result.passed))
        # print("end test status:{}".format(result.status))
        self.conn.hset(self.case_redis_key, data.doc, result.status)

    def end_suite(self, data, result):
        # print("end suite data: {}".format(dir(data)))
        # print("end suite result: {}".format(dir(result)))
        if not result.parent:
            stat = suite_result_handler(result.full_message)
            app.send_task(
                'task.tasks.robot_notifier',
                queue='notifier',
                args=(self.build_id,),
                kwargs={
                    'status': 0,
                    'failed_case': stat.get('failed', 0),
                    'passed_case': stat.get('passed', 0),
                    'skipped_case': stat.get('skipped', 0),
                    'elapsed_case': stat.get('elapsed', 0),
                    'end_time': datetime.now().timestamp()
                }
            )

    def close(self):
        pass
