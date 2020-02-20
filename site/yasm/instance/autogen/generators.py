import shutil
from trie import *
from declarative import Message, Enum, Service


def build_frontend(env, path):
    interface_template = env.get_template('frontend/interface.ts.jinja2')
    enum_template = env.get_template('frontend/enum.ts.jinja2')
    bundle_interfaces_template = env.get_template('frontend/bundle_interfaces.ts.jinja2')
    bundle_services_template = env.get_template('frontend/bundle_services.ts.jinja2')
    service_template = env.get_template('frontend/service.ts.jinja2')
    front_trie = Trie()
    for message in Message.root_level_registry.values():
        if not message.is_internal:
            front_trie = add_trie_item(front_trie, message.package.split('.'), message)
    for enum in Enum.root_level_registry.values():
        if not enum.is_internal:
            front_trie = add_trie_item(front_trie, enum.package.split('.'), enum)

    def message_to_interfaces(item, level=0):
        if isinstance(item, Message):
            return interface_template.render(message=item)
        if isinstance(item, Enum):
            return enum_template.render(enum=item)

    def bundle_interfaces(
            level,
            bundle,
            children,
            *args,
    ):
        return bundle_interfaces_template.render(
            level='../' * level,
            bundle=bundle,
            children=children,
        )

    interfaces_path = os.path.join(path, 'interfaces')
    if os.path.exists(interfaces_path):
        shutil.rmtree(interfaces_path, ignore_errors=True)

    front_trie.traverse(
        path=interfaces_path,
        file_name='index.ts',
        item_map=message_to_interfaces,
        directory_map=bundle_interfaces,
    )
    service_trie = Trie()
    for service in Service.registry.values():
        service_trie = add_trie_item(service_trie, service.package.split('.'), service)

    def service_to_ts(service, level):
        return service_template.render(service=service)

    def bundle_services(
            level,
            bundle,
            children,
            *args,
    ):
        return bundle_services_template.render(
            level='../' * level,
            bundle=bundle,
            children=children,
        )

    services_path = os.path.join(path, 'services')
    if os.path.exists(services_path):
        shutil.rmtree(services_path, ignore_errors=True)

    service_trie.traverse(
        path=services_path,
        file_name='index.ts',
        item_map=service_to_ts,
        directory_map=bundle_services,
    )
    print('frontend done')


def build_api(env, path):
    service_trie = Trie()
    for service in Service.registry.values():
        service_trie = add_trie_item(service_trie, service.package.split('.'), service)

    service_template = env.get_template('flask/service.py.jinja2')
    bundle_template = env.get_template('flask/bundle.py.jinja2')

    def service_to_flask(service, level):
        return service_template.render(service=service, level='.' * level)

    def bundle_services(
            level,
            bundle,
            children,
            name,
    ):
        return bundle_template.render(
            name=name,
            level=level,
            services=[service[:-3] for service in bundle],
            children=children,
        )

    if os.path.exists(path):
        shutil.rmtree(path, ignore_errors=True)

    service_trie.traverse(
        path=path,
        file_name='__init__.py',
        item_map=service_to_flask,
        directory_map=bundle_services,
        separate_items=True,
        get_item_name=lambda service, level: service.python_name + '.py'
    )
    print('api done')

