from datetime import datetime
from celeryapp import app
from robot.run import run
from plugin.RobotListener import RobotListener
from handler.filehandler import variable_file_checker


@app.task
def robot_runner(project, env, region, task_id, batch_no, run_suite, run_data, variable_files, external_files):
    """execute test"""
    var_files = variable_file_checker(env, region, variable_files)
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    output_file = f'{now}_{task_id}_{batch_no}.xml'
    run(*run_suite,
        project=project,
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
        variablefile=var_files,
        listener=RobotListener(task_id),
        )


@app.task
def robot_notifier(task_id, project, env, region):
    """robot notice task, no logic needed here, master will do it"""
    pass


