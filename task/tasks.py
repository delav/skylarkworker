from datetime import datetime
from celeryapp import app
from robot.run import run
from plugin.RobotListener import RobotListener
from plugin.RebotModifier import RobotModifier


@app.task(bind=True)
def robot_runner(self, build_id, run_suite, meta_data, report_path):
    app.send_task(
        'task.tasks.robot_notifier',
        queue='notifier',
        args=(build_id,),
        kwargs={'start_time': datetime.now().timestamp(), 'status': 1}
    )
    run(*run_suite,
        outputdir=report_path,
        metadata=meta_data,
        listener=RobotListener(build_id),)
        # prerebotmodifier=RobotModifier())  # UserWarning: 'keywords' attribute is read-only and deprecated since Robot Framework 4.0. Use 'body', 'setup' or 'teardown' instead.


@app.task(bind=True)
def robot_notifier(self, task_id, msg_type):
    """robot notice task, no logic needed here, master will do it"""
    pass


