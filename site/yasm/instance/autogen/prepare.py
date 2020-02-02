import os
import sys
import shutil
import tempfile
import subprocess
import importlib

from declarative import AutogenOptions, File


# TMP_ROOT = tempfile.mkdtemp()
TMP_ROOT = os.path.join(os.getcwd(), '__TMP__')


def build_py_proto(spec_path):

    path = TMP_ROOT

    if os.path.exists(path):
        shutil.rmtree(path, ignore_errors=True)
    os.makedirs(path)

    cwd = os.getcwd()
    os.chdir(spec_path)
    command = [
        'protoc',
        *get_proto_files(spec_path),
        f'--python_out={path}',
    ]
    print(' '.join(command))
    p = subprocess.Popen(command)
    p.wait()
    p.communicate()
    os.chdir(cwd)


def map_proto_2_py(path):
    return path.replace('/', '.')[:-6] + '_pb2'


def get_proto_files(spec_path):
    return [
        os.path.join(d[0][len(spec_path) + 1:], f)
        for d in os.walk(spec_path)
        for f in d[-1]
        if f.endswith('.proto')
    ]


def get_py_files(spec_path):
    return [
        map_proto_2_py(file)
        for file in get_proto_files(spec_path)
    ]


def load_py_proto(spec_path):
    build_py_proto(spec_path)
    old_path = sys.path
    sys.path = [
        TMP_ROOT,
        *[
            path
            for path in old_path
            if not path.endswith('instance') and path
        ]
    ]
    modules = []
    for file in get_py_files(spec_path):
        modules.append(importlib.import_module(file))
        if file == 'lib.api_pb2':
            AutogenOptions.API.load(modules[-1])
        elif file == 'lib.database_pb2':
            AutogenOptions.Database.load(modules[-1])
    ret = [
        File(file.DESCRIPTOR)
        for file in modules
    ]
    sys.path = old_path
    return ret, modules