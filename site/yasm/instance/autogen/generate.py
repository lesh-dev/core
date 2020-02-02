import os
import jinja2

from prepare import load_py_proto
from declarative import link
from generators import build_api, build_frontend


ROOT = os.getcwd()
API_ROOT = 'generated'
PB_ROOT = 'generated'
FRONT_ROOT = 'generated'
SPEC_PATH = os.path.join(ROOT, 'specs')


def main():
    files, modules = load_py_proto(SPEC_PATH)
    link()

    print("load done")
    template_env = jinja2.Environment(
        loader=jinja2.PackageLoader('autogen', 'templates'),
        trim_blocks=True
    )
    build_frontend(template_env, os.path.join(FRONT_ROOT, 'frontend'))
    build_api(template_env, os.path.join(API_ROOT, 'api'))

    print('done')


if __name__ == '__main__':
    main()


