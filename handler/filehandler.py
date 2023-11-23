import os
import re
import asyncio
import json
import base64
from datetime import datetime
from pathlib import Path
from aiohttp import ClientSession
from settings import FILE_DIR


def variable_file_maker(file_map, env, region, args):
    """
    check whether the variable files need to be updated
    """
    if not isinstance(file_map, dict):
        try:
            file_map = json.loads(file_map)
        except (Exception,):
            return []
    absolute_file = []
    args = args.strip()
    for path_name, file_text in file_map.items():
        file = Path(FILE_DIR, path_name)
        file_dir = file.parent
        if path_name.endswith('.py'):
            file_and_arg = f'{file}:{env}:{region}'
            if args:
                file_and_arg = file_and_arg + f':{args}'
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


def project_file_maker(file_map):
    asyncio.run(download_many_by_file_map(file_map))


async def download_many_by_file_map(file_map):
    """
    check whether the project files need to be downloaded from master
    """
    if not isinstance(file_map, dict):
        try:
            file_map = json.loads(file_map)
        except (Exception,):
            return []
    task_list = []
    async with ClientSession() as session:
        for path_name, file_info in file_map.items():
            file = Path(FILE_DIR, path_name)
            file_dir = file.parent
            if not file.is_file():
                task = asyncio.create_task(download_file_form_master(session, file_info, file, file_dir))
                task_list.append(task)
                continue
            file_mtime = file.stat().st_mtime
            if file_mtime != file_info.get('mtime'):
                task = asyncio.create_task(download_file_form_master(session, file_info, file, file_dir))
                task_list.append(task)
        results = await asyncio.gather(*task_list)
        return len(results)


async def download_file_form_master(session, file_info, file, file_dir):
    """
    download project file from master
    """
    headers = {
        'auth': base64_encrypt(file_info.get('key', ''))
    }
    request_url = file_info.get('url', '')
    request_params = file_info.get('params', {})
    pattern = r'^https?://[\w\-]+(\.[\w\-]+)+[/#?]?.*$'
    if not re.match(pattern, request_url):
        return
    try:
        async with session.post(
                url=request_url,
                headers=headers,
                data=request_params
        ) as r:
            response = await r.read()
    except (Exception,):
        return
    if not file_dir.is_dir():
        file_dir.mkdir(parents=True, exist_ok=True)
    destination = open(file, 'wb+')
    destination.write(response)
    destination.close()
    mtime = file_info.get('mtime', int(datetime.now().timestamp()))
    os.utime(file, (int(datetime.now().timestamp()), mtime))


def base64_encrypt(input_str):
    input_bytes = input_str.encode('utf-8')
    base64_bytes = base64.b64encode(input_bytes)
    base64_str = base64_bytes.decode('utf-8')
    return base64_str
