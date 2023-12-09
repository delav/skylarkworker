from celeryapp import app


@app.task
def heartbeat(ip_addr):
    pass


@app.task
def worker_collector(info_type, info):
    pass


@app.task
def command_executor(cmd):
    pass
