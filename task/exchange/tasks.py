from handler.gitclient import GitClient
from settings import LIBRARY_GIT, LIBRARY_PATH
from celeryapp import app


@app.task
def heartbeat(ip_addr):
    pass


@app.task
def worker_collector(info_type, info):
    pass


@app.task
def command_executor(cmd):
    if cmd == 'git':
        _update_library_repository()


def _update_library_repository():
    max_retry = 3
    git_client = GitClient()
    try_count = 0
    update_flag = False
    if not LIBRARY_PATH.exists():
        while try_count < max_retry:
            try:
                git_client.clone(LIBRARY_GIT, LIBRARY_PATH)
                update_flag = True
            except (Exception,):
                try_count += 1
                continue
            break
    else:
        while try_count < max_retry:
            try:
                git_client.pull(LIBRARY_PATH)
                update_flag = True
            except (Exception,):
                try_count += 1
                continue
            break
    return update_flag
