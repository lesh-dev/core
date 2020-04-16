import os
import sys
import shutil
import tempfile
import subprocess
import importlib

from instance.autogen.declarative import link, AutogenOptions, Package, Service, File, Message, Enum


TMP_ROOT = tempfile.mkdtemp()
TMP_PY = os.path.join(TMP_ROOT, 'py')
TMP_PROTO = os.path.join(TMP_ROOT, 'proto')

google_proto_files = [
    'google/protobuf/empty.proto'
]


def copy_proto(spec_path):
    shutil.copytree(spec_path, TMP_PROTO)


def build_py_proto():
    if os.path.exists(TMP_PY):
        shutil.rmtree(TMP_PY, ignore_errors=True)
    os.makedirs(TMP_PY)

    cwd = os.getcwd()
    os.chdir(TMP_PROTO)
    command = [
        'protoc',
        *get_proto_files(TMP_PROTO),
        f'--python_out={TMP_PY}',
    ]
    print(' '.join(command))
    p = subprocess.Popen(command)
    p.wait()
    p.communicate()
    os.chdir(cwd)


def map_proto_2_py(path):
    return path.replace('/', '.')[:-6] + '_pb2'


def get_proto_files(spec_path):
    return google_proto_files + [
        os.path.join(d[0][len(spec_path) + 1:], f)
        for d in os.walk(spec_path)
        for f in d[-1]
        if f.endswith('.proto')
    ]


def get_py_files():
    return [
        map_proto_2_py(file)
        for file in get_proto_files(TMP_PROTO)
    ]


def load_py_proto():
    build_py_proto()
    old_path = sys.path
    sys.path = [
        TMP_PY,
        *[
            path
            for path in old_path
            if not path.endswith('instance') and path
        ]
    ]
    modules = []
    for file in get_py_files():
        modules.append(importlib.import_module(file))
        if file == 'lib.api_pb2':
            AutogenOptions.API.load(modules[-1])
        elif file == 'lib.database_pb2':
            AutogenOptions.Database.load(modules[-1])
        elif file == 'lib.plain_types_pb2':
            AutogenOptions.Types.load(modules[-1])
    ret = [
        File(file.DESCRIPTOR)
        for file in modules
    ]
    sys.path = old_path
    return ret, modules


def create_builtin(template_env):
    builtins_template = template_env.get_template('proto/builtins.proto.jinja2')
    with open(os.path.join(TMP_PROTO, 'builtins.proto'), 'w') as builtins:
        builtins.write(builtins_template.render(messages=Message.registry))


def clear_registry():
    Package.clear_registry()
    Message.clear_registry()
    Enum.clear_registry()
    Service.clear_registry()
    File.clear_registry()


def load(spec_path, template_env):
    copy_proto(spec_path)
    load_py_proto()
    create_builtin(template_env)
    clear_registry()
    files, modules = load_py_proto()
    link()
