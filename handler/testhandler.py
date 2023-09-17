import os
import json
from datetime import datetime
from celeryapp import app
from settings import ROBOT_REDIS_URL, TASK_RESULT_KEY_PREFIX, REDIS_EXPIRE_TIME
from settings import NOTIFIER_QUEUE, NOTIFIER_TASK, NOTIFIER_ROUTING_KEY
from handler.redisclient import RedisClient


class TestHandler(object):

    def __init__(self, task_id, batch_no, project, env, region):
        self.task_id = task_id
        self.batch_no = batch_no
        self.project = project
        self.env = env
        self.region = region
        self.conn = RedisClient(ROBOT_REDIS_URL).connector

    def start_testing(self):
        self.start_time = datetime.now().timestamp()

    def end_testing(self, stat_message, output):
        output_ctx = self._read_from_file(output)
        stat = self._stat_parser(stat_message)
        redis_key = TASK_RESULT_KEY_PREFIX + self.task_id
        batch_result = {
            'start_time': self.start_time,
            'failed': stat.get('failed', 0),
            'passed': stat.get('passed', 0),
            'skipped': stat.get('skipped', 0),
            'end_time': datetime.now().timestamp(),
            'output': output_ctx,
        }
        filed = self.task_id + '_' + self.batch_no
        self.conn.hset(redis_key, filed, json.dumps(batch_result))
        self.conn.expire(redis_key, REDIS_EXPIRE_TIME)
        app.send_task(
            NOTIFIER_TASK,
            queue=NOTIFIER_QUEUE,
            routing_key=NOTIFIER_ROUTING_KEY,
            args=(self.task_id, self.project, self.env, self.region),
        )

    def _stat_parser(self, result_str):
        state_count = {}
        state_strs = result_str.split(',')
        for item in state_strs:
            cs = item.split()
            state_count[cs[1]] = cs[0]
        return state_count

    def _read_from_file(self, file_path):
        f = open(file_path, 'r', encoding='utf-8')
        _text = f.read()
        f.close()
        os.remove(file_path)
        return _text
