from datetime import datetime
from celeryapp import app
from robot.run import run
from settings import FILE_DIR
from plugin.RobotListener import RobotListener
from handler.filehandler import variable_file_maker, project_file_maker


@app.task
def robot_runner(project, env, region, args, task_id,
                 batch_no, run_suite, run_data, variable_files, external_files):
    """execute test"""
    project_file_dir = (FILE_DIR / project).as_posix()
    var_files = variable_file_maker(variable_files, env, region, args)
    project_file_maker(external_files)
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
        filedir=project_file_dir,
        listener=RobotListener(task_id),
        )


@app.task
def robot_notifier(task_id, project, env, region, notify_type):
    """robot notice task, no logic needed here, master will do it"""
    pass


