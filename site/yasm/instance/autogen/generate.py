import os
import shutil
import inflection
import jinja2
import subprocess
from google.protobuf.descriptor_pb2 import FileDescriptorSet
from google.protobuf.descriptor import FieldDescriptor

API_ROOT = 'generated'
PB_ROOT = 'generated'
FRONT_ROOT = 'generated'
SPEC_PATH = 'specs'

proto_files = dict()


class Package:
    service_registry = set()
    item_registry = set()


class Method:
    def __init__(self, method, service):
        self.descriptor = method
        self.service = service
        self.name = method.name
        self.url = f'{service.fqdn}.{self.name}'.replace('.', '/')
        self.input_type = method.input_type
        self.output_type = method.output_type
        self.input_message = None
        self.output_message = None

    @property
    def python_name(self):
        return inflection.underscore(self.name)


class Service:
    registry = dict()

    def __init__(self, service, package):
        self.descriptor = service
        self.name = service.name
        self.methods = []
        self.package = package
        Package.service_registry.add(package)
        self.fqdn = f'.{self.package}.{self.name}'
        Service.registry[self.fqdn] = self
        for method in service.method:
            self.methods.append(Method(method, self))

    @property
    def python_name(self):
        return inflection.underscore(self.name)


class Value:
    def __init__(self, value):
        self.descriptor = value
        self.name = value.name
        self.number = value.number


class Enum:
    registry = dict()
    root_level_registry = dict()

    def __init__(self, enum, package, parent=None):
        self.descriptor = enum
        self.name = enum.name
        self.package = package
        Package.item_registry.add(package)
        self.parent = parent
        self.fqdn = ''.join([
            f'.{self.package}',
            f'.{self.parent.name}' if self.parent is not None else '',
            f'.{self.name}'
        ])
        if parent is None:
            Enum.root_level_registry[self.fqdn] = self
        Enum.registry[self.fqdn] = self
        self.values = []
        for value in enum.value:
            self.values.append(Value(value))


class Field:
    def __init__(self, field):
        self.descriptor = field
        self.name = field.name
        self.number = field.number
        self.label = field.label
        self.type = field.type
        self.type_name = field.type_name
        self.json_name = field.json_name
        self.label = field.label
        self.enum = None
        self.message = None

    def is_enum(self):
        return self.type == FieldDescriptor.TYPE_ENUM

    def is_message(self):
        return self.type == FieldDescriptor.TYPE_MESSAGE

    @property
    def actual_type(self):
        if self.is_enum():
            return self.enum
        if self.is_message():
            return self.message
        return self.type

    @property
    def ts_type(self):
        repeated = ''
        if self.label == FieldDescriptor.LABEL_REPEATED:
            repeated = '[]'
        if self.is_enum():
            return f'interfaces{self.enum.fqdn}{repeated}'
        if self.is_message():
            if self.message.options.map_entry:
                key = None
                value = None
                for field in self.message.fields:
                    if field.name == 'key':
                        key = field
                    if field.name == 'value':
                        value = field
                return f'{{[index: {key.ts_type}]: {value.ts_type}}}'
            return f'interfaces{self.message.fqdn}{repeated}'
        if self.type == FieldDescriptor.TYPE_BOOL:
            return f'boolean{repeated}'
        if self.type == FieldDescriptor.TYPE_STRING:
            return f'string{repeated}'
        return f'number{repeated}'


class MessageOptions:
    def __init__(self, options, message):
        self.descriptor = options
        self.message = message
        self.map_entry = options.map_entry


class Message:
    registry = dict()
    root_level_registry = dict()

    def __init__(self, message, package, parent=None):
        self.descriptor = message
        self.name = message.name
        self.parent = parent
        self.package = package
        Package.item_registry.add(package)
        if parent is not None:
            self.fqdn = f'{parent.fqdn}.{self.name}'
        else:
            self.fqdn = f'.{self.package}.{self.name}'
        Message.registry[self.fqdn] = self
        if parent is None:
            Message.root_level_registry[self.fqdn] = self
        self.options = MessageOptions(message.options, message)
        self.fields = []
        for field in message.field:
            self.fields.append(Field(field))
        self.nested_messages = []
        for nested in message.nested_type:
            self.nested_messages.append(Message(nested, package=package, parent=self))
        self.nested_enums = []
        for nested in message.enum_type:
            self.nested_enums.append(Enum(nested, package=package, parent=self))


class File:
    def __init__(self, file):
        self.descriptor = file
        self.name = file.name
        self.package = file.package
        self.messages = []
        for message in file.message_type:
            self.messages.append(Message(message, package=self.package))
        self.enums = []
        for enum in file.enum_type:
            self.enums.append(Enum(enum, package=self.package))
        self.services = []
        for service in file.service:
            self.services.append(Service(service, package=self.package))


class Trie:
    def __init__(self):
        self._items = []
        self._children = None

    def get(self, parts, fallback=None):
        if len(parts) == 0:
            return self
        if fallback is None:
            fallback = Trie()
        if self._children is None:
            self._children = dict()
        if type(parts) == str:
            return self._children.get(parts, fallback)
        first, *others = parts
        if first not in self._children:
            self._children[first] = fallback
        return self._children[first].get(others)

    def append(self, item):
        self._items.append(item)

    def keys(self):
        if self._children is None:
            return []
        return self._children.keys()

    def items(self):
        if self._children is None:
            return []
        return self._children.items()

    def traverse(
            self,
            path,
            file_name,
            item_map,
            directory_map,
            level=0,
            separate_items=False,
            get_item_name=None
    ):
        mapper = item_map
        if separate_items:
            assert get_item_name is not None
            mapper = get_item_name
        os.makedirs(path)
        if file_name is not None and directory_map is not None:
            index = directory_map(
                level,
                [mapper(item) for item in self._items],
                self.keys(),
                os.path.basename(path),
            )
            with open(os.path.join(path, file_name), 'w') as file:
                file.write(index)
        if separate_items:
            for item in self._items:
                with open(os.path.join(path, get_item_name(item)), 'w') as file:
                    file.write(item_map(item))
        for name, trie in self.items():
            trie.traverse(
                path=os.path.join(path, name),
                file_name=file_name,
                item_map=item_map,
                directory_map=directory_map,
                level=level + 1,
                separate_items=separate_items,
                get_item_name=get_item_name
            )


def add_trie_path(trie, parts):
    if len(parts) == 0:
        return trie
    first, *other = parts
    trie._children[first] = add_trie_path(trie.get(first), other)
    return trie


def add_trie_item(trie, path, item):
    trie.get(path).append(item)
    return trie


def build_descriptor():
    cwd = os.getcwd()
    os.chdir(SPEC_PATH)
    path = os.path.normpath(os.path.join(os.getcwd(), 'descriptor.pb2'))

    command = [
        'protoc',
        'bundle.proto',
        '--include_imports',
        '--include_source_info',
        f'--descriptor_set_out={path}',
    ]
    print(' '.join(command))
    p = subprocess.Popen(command)
    p.wait()
    p.communicate()
    os.chdir(cwd)
    return path


def build_frontend(env, path=os.path.join(FRONT_ROOT, 'frontend')):
    interface_template = env.get_template('frontend/interface.ts.jinja2')
    enum_template = env.get_template('frontend/enum.ts.jinja2')
    bundle_interfaces_template = env.get_template('frontend/bundle_interfaces.ts.jinja2')
    bundle_services_template = env.get_template('frontend/bundle_services.ts.jinja2')
    service_template = env.get_template('frontend/service.ts.jinja2')
    front_trie = Trie()
    for message in Message.root_level_registry.values():
        front_trie = add_trie_item(front_trie, message.package.split('.'), message)
    for enum in Enum.root_level_registry.values():
        front_trie = add_trie_item(front_trie, enum.package.split('.'), enum)

    def message_to_interfaces(item):
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

    def service_to_ts(service):
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


def build_api(env, path=os.path.join(API_ROOT, 'api')):
    service_trie = Trie()
    for service in Service.registry.values():
        service_trie = add_trie_item(service_trie, service.package.split('.'), service)

    service_template = env.get_template('flask/service.py.jinja2')
    bundle_template = env.get_template('flask/bundle.py.jinja2')

    def service_to_flask(service):
        return service_template.render(service=service)

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
        get_item_name=lambda service: service.python_name + '.py'
    )
    print('api done')


def main():
    with open(build_descriptor(), 'rb') as fds:
        bundle = FileDescriptorSet.FromString(fds.read())
    for file in bundle.file:
        proto_files[file.name] = File(file)
    print("build done")
    for fqdn, message in Message.registry.items():
        for field in message.fields:
            if field.is_message():
                field.message = Message.registry[field.type_name]
            if field.is_enum():
                field.enum = Enum.registry[field.type_name]
    for fqdn, service in Service.registry.items():
        for method in service.methods:
            method.input_message = Message.registry[method.input_type]
            method.output_message = Message.registry[method.output_type]
    print('linkage done')
    template_env = jinja2.Environment(
        loader=jinja2.PackageLoader('autogen', 'templates'),
        trim_blocks=True
    )
    build_frontend(template_env)
    build_api(template_env)

    print('done')


if __name__ == '__main__':
    main()