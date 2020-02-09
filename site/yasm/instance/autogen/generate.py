import os
import shutil
import jinja2

from prepare import load_py_proto
from trie import Trie, add_trie_item
from declarative import link, Message
from generators import build_api, build_frontend


ROOT = os.getcwd()
API_ROOT = 'generated'
DB_ROOT = 'generated/database'
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

    database_trie = Trie()
    for database_message in Message.database:
        database_trie = add_trie_item(database_trie, database_message.package.split('.')[2:], database_message)

    path = os.path.join(ROOT, DB_ROOT)
    if os.path.exists(path):
        shutil.rmtree(path, ignore_errors=True)

    db_template = template_env.get_template('database/database.py.jinja2')
    model_template = template_env.get_template('database/model.py.jinja2')

    def message_to_model(message):
        return model_template.render(message=message)

    def bundle_db(
            level,
            bundle,
            *args,
    ):
        return db_template.render(
            models=bundle,
        )

    database_trie.traverse(
        path=path,
        file_name='database.py',
        item_map=message_to_model,
        directory_map=bundle_db,
    )

    print('done')


if __name__ == '__main__':
    main()


