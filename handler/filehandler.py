import os
import asyncio
import json
from aiohttp import request
from datetime import datetime
from pathlib import Path
from settings import FILE_DIR

PATH_SEPARATOR = '/'
SEMAPHORE_NUMBER = 8


def async_handler(*args: tuple):
    """
    async request handler with event loop
    """
    task_list = []
    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)
    event_loop = asyncio.get_event_loop()
    sem = asyncio.Semaphore(SEMAPHORE_NUMBER)
    for item in args:
        func, arg = item[0], item[1:]
        task = asyncio.ensure_future(
            func(sem, *arg))
        task_list.append(task)
    results = event_loop.run_until_complete(
        asyncio.gather(*task_list)
    )
    event_loop.close()
    return dict(results)


def variable_file_checker(env, region, file_map):
    """
    check whether the variable files need to be updated
    """
    if not isinstance(file_map, dict):
        try:
            file_map = json.loads(file_map)
        except (Exception,):
            return
    absolute_file = []
    for file_name, file_text in file_map.items():
        file, file_dir = get_file_and_path(file_name)
        if file_name.endswith('.py'):
            file_and_arg = f'{file}:{env}:{region}'
            absolute_file.append(file_and_arg)
        else:
            absolute_file.append(f'{file}')
        if file.is_file():
            continue
        if not file_dir.is_dir():
            file_dir.mkdir(parents=True, exist_ok=True)
        destination = open(file, 'wb+')
        destination.write(file_text.encode())
        destination.close()
    return absolute_file


def project_file_checker(file_map):
    """
    check whether the project files need to be downloaded from master
    """
    if not isinstance(file_map, dict):
        try:
            file_map = json.loads(file_map)
        except (Exception,):
            return
    re_download_files = []
    for file_name, file_info in file_map.items():
        file, file_dir = get_file_and_path(file_name)
        if not file.is_file():
            re_download_files.append(
                (download_file_form_master, file_info, file, file_dir)
            )
            continue
        file_mtime = file.stat().st_mtime
        if file_mtime != file_info.get('mtime'):
            re_download_files.append(
                (download_file_form_master, file_info, file, file_dir)
            )
    async_handler(*re_download_files)


def get_file_and_path(file_str):
    """
    get file name and file dir
    """
    child_path = file_str.split(PATH_SEPARATOR)
    relative_path = child_path[:-1]
    file_dir = Path(FILE_DIR, *relative_path)
    file = Path(FILE_DIR, *child_path)
    return file, file_dir


async def download_file_form_master(sem, file_info, file, file_dir):
    """
    download project file from master
    """
    headers = {}
    request_url = file_info.get('host') + file_info.get('api')
    request_params = file_info.get('params')
    async with sem:
        try:
            async with request(
                    method='POST',
                    url=request_url,
                    headers=headers,
                    data=request_params
            ) as r:
                response = await r.json(content_type='text/html', encoding='utf-8')
                if not file_dir.is_dir():
                    file_dir.mkdir(parents=True, exist_ok=True)
                destination = open(file, 'wb+')
                destination.write(response.encode())
                destination.close()
                os.utime(file, (int(datetime.now().timestamp()), file_info.get('mtime')))
        except (Exception,):
            pass

