import os
import shutil
import jinja2

from prepare import load_py_proto
from trie import Trie, add_trie_item
from declarative import link, Message
from generators import build_api, build_frontend

from declarative import Enum


ROOT = os.getcwd()
API_ROOT = 'generated'
GEN_ROOT = 'generated'
FRONT_ROOT = 'ui/src/js/generated'
SPEC_PATH = os.path.join(ROOT, 'specs')


def main():
    files, modules = load_py_proto(SPEC_PATH)
    link()

    print("load done")
    template_env = jinja2.Environment(
        loader=jinja2.PackageLoader('instance.autogen', 'templates'),
        trim_blocks=True
    )
    build_frontend(template_env, os.path.join(FRONT_ROOT, 'frontend'))
    build_api(template_env, os.path.join(API_ROOT, 'api'))

    py_message_trie = Trie()
    py_enum_trie = Trie()
    for message in Message.root_level_registry.values():
        if not message.is_internal:
            py_message_trie = add_trie_item(py_message_trie, message.package.split('.'), message)
    for enum in Enum.root_level_registry.values():
        if not enum.is_internal:
            py_enum_trie = add_trie_item(py_enum_trie, enum.package.split('.'), enum)

    path = os.path.join(ROOT, GEN_ROOT)
    enums_path = os.path.join(path, 'enums')
    models_path = os.path.join(path, 'models')
    if os.path.exists(enums_path):
        shutil.rmtree(enums_path, ignore_errors=True)
    if os.path.exists(models_path):
        shutil.rmtree(models_path, ignore_errors=True)

    module_template = template_env.get_template('database/module.py.jinja2')
    enum_module_template = template_env.get_template('database/enum_module.py.jinja2')
    stub_template = template_env.get_template('database/stub.py.jinja2')
    root_template = template_env.get_template('root.py.jinja2')
    model_template = template_env.get_template('database/message.py.jinja2')
    enum_template = template_env.get_template('database/enum.py.jinja2')

    def enumeration(enum, level):
        return enum_template.render(enum=enum)

    def bundle_enums(
            level,
            bundle,
            children,
            *args,
    ):
        return enum_module_template.render(
            level='.' * level,
            enums=bundle,
            children=children,
        )

    py_enum_trie.traverse(
        path=enums_path,
        file_name='__init__.py',
        item_map=enumeration,
        directory_map=bundle_enums,
    )

    def message_to_model(message, level):
        return model_template.render(message=message)

    def bundle_db(
            level,
            bundle,
            children,
            *args,
    ):
        return module_template.render(
            level='.' * level,
            models=bundle,
            children=children,
        )

    py_message_trie.traverse(
        path=models_path,
        file_name='__init__.py',
        item_map=message_to_model,
        directory_map=bundle_db,
    )

    with open(os.path.join(models_path, 'stub.py'), 'w') as stub:
        stub.write(stub_template.render())

    with open(os.path.join(GEN_ROOT, '__init__.py'), 'w') as stub:
        stub.write(root_template.render())

    print('done')


if __name__ == '__main__':
    main()


