from datetime import datetime
from celeryapp import app
from robot.run import run
from plugin.RobotListener import RobotListener


@app.task
def robot_runner(env, region, task_id, batch_no, run_suite, run_data):
    """execute test"""
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    output_file = f'{now}_{task_id}_{batch_no}.xml'
    run(*run_suite,
        environment=env,
        region=region,
        outputdir='output',
        output=output_file,
        report=None,
        log=None,
        console='quiet',
        taskid=task_id,
        batch=batch_no,
        sources=run_data,
        listener=RobotListener(task_id),
        )


@app.task
def robot_notifier(task_id):
    """robot notice task, no logic needed here, master will do it"""
    pass


