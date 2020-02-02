from google.protobuf.descriptor import FieldDescriptor
from collections import OrderedDict
import inflection


class AutogenOptions:
    class Database:
        db_table = None
        login_table = None
        primary_key = None
        foreign_key_field = None
        foreign_key_table = None
        lazy_load = None
        searchable = None
        LazyLoad = None

        @staticmethod
        def load(module):
            AutogenOptions.Database.db_table = module.db_table
            AutogenOptions.Database.login_table = module.login_table
            AutogenOptions.Database.primary_key = module.primary_key
            AutogenOptions.Database.foreign_key_field = module.foreign_key_field
            AutogenOptions.Database.foreign_key_table = module.foreign_key_table
            AutogenOptions.Database.lazy_load = module.lazy_load
            AutogenOptions.Database.searchable = module.searchable
            AutogenOptions.Database.LazyLoad = module.LazyLoad

    class API:
        file_require_login = None
        file_before_request = None
        file_after_request = None
        service_require_login = None
        service_before_request = None
        service_after_request = None
        method_require_login = None
        method_before_request = None
        method_after_request = None

        @staticmethod
        def load(module):
            AutogenOptions.API.file_require_login = module.file_require_login
            AutogenOptions.API.file_before_request = module.file_before_request
            AutogenOptions.API.file_after_request = module.file_after_request
            AutogenOptions.API.service_require_login = module.service_require_login
            AutogenOptions.API.service_before_request = module.service_before_request
            AutogenOptions.API.service_after_request = module.service_after_request
            AutogenOptions.API.method_require_login = module.method_require_login
            AutogenOptions.API.method_before_request = module.method_before_request
            AutogenOptions.API.method_after_request = module.method_after_request


class Meta:
    @property
    def is_internal(self):
        return self.full_name.startswith('yasm.lib')

    def __repr__(self):
        return f'{self.__class__.__name__}--{self.name or ""}'

    __str__ = __repr__


class Package:
    service_registry = set()
    item_registry = set()


class Method(Meta):
    def __init__(self, method, service):
        self.descriptor = method
        self.service = service
        self.name = method.name
        self.url = f'{service.full_name}.{self.name}'.replace('.', '/')
        self.input_type = method.input_type
        self.output_type = method.output_type
        self.input_message = None
        self.output_message = None

    @property
    def python_name(self):
        return inflection.underscore(self.name)


class Service(Meta):
    registry = OrderedDict()

    def __init__(self, service, package):
        self.descriptor = service
        self.name = service.name
        self.package = package
        Package.service_registry.add(package)
        self.full_name = service.full_name
        Service.registry[self.full_name] = self
        self.methods = OrderedDict()
        for method_name, method in service.methods_by_name.items():
            self.methods[method_name] = Method(method, self)

    @property
    def python_name(self):
        return inflection.underscore(self.name)


class Value(Meta):
    def __init__(self, value):
        self.descriptor = value
        self.name = value.name
        self.number = value.number


class Enum(Meta):
    registry = OrderedDict()
    root_level_registry = OrderedDict()

    def __init__(self, enum, package, parent=None):
        self.descriptor = enum
        self.name = enum.name
        self.package = package
        Package.item_registry.add(package)
        self.parent = parent
        self.full_name = enum.full_name
        if parent is None:
            Enum.root_level_registry[self.full_name] = self
        Enum.registry[self.full_name] = self
        self.values = OrderedDict()
        for value_name, value in enum.values_by_name.items():
            self.values[value_name] = Value(value)


class Field(Meta):
    def __init__(self, field, message):
        self.descriptor = field
        self.name = field.name
        self.number = field.number
        self.label = field.label
        self.type = field.type
        self.label = field.label
        self.message = None
        if field.message_type is not None:
            self.message = field.message_type
        self.enum = None
        if field.enum_type is not None:
            self.enum = field.enum_type
        self.message_obj = None
        self.enum_obj = None
        # self.options = object()
        # self.options.primary_key = field.GetOptions().Extensions[AutogenOptions.Database.primary_key]
        # self.options.foreign_key_field = field.GetOptions().Extensions[AutogenOptions.Database.foreign_key_field]
        # self.options.foreign_key_table = field.GetOptions().Extensions[AutogenOptions.Database.foreign_key_table]
        # self.options.lazy_load = field.GetOptions().Extensions[AutogenOptions.Database.lazy_load]
        # self.options.searchable = field.GetOptions().Extensions[AutogenOptions.Database.searchable]

        # if not message.options.database:
        #     if self.options.primary_key or self.options.foreign_key_field or self.options.foreign_key_table or self.options.lazy_load:
        #         raise RuntimeError('database options in {} of {}, which is not a db_table'.format(self, message))
        # if (self.options.foreign_key_table == '') ^ (self.options.foreign_key_field == ''):
        #     raise RuntimeError('can not have only one of foreign_key_table and foreign_key_field at {} in {}'.format(self, message))

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
            return f'interfaces.{self.enum.full_name}{repeated}'
        if self.is_message():
            if self.message_obj.options.map_entry:
                key = None
                value = None
                for field in self.message_obj.fields.values():
                    if field.name == 'key':
                        key = field
                    if field.name == 'value':
                        value = field
                return f'{{[index: {key.ts_type}]: {value.ts_type}}}'
            return f'interfaces.{self.message.full_name}{repeated}'
        if self.type == FieldDescriptor.TYPE_BOOL:
            return f'boolean{repeated}'
        if self.type == FieldDescriptor.TYPE_STRING:
            return f'string{repeated}'
        return f'number{repeated}'


class MessageOptions(Meta):
    def __init__(self, options, message):
        self.descriptor = options
        self.message = message
        self.map_entry = options.map_entry
        self.database = options.Extensions[AutogenOptions.Database.db_table]
        self.login = options.Extensions[AutogenOptions.Database.login_table]


class Message(Meta):
    registry = OrderedDict()
    root_level_registry = OrderedDict()
    database = []
    login_table = None

    def __init__(self, message, package, parent=None):
        self.descriptor = message
        self.name = message.name
        self.parent = parent
        self.package = package
        self.full_name = message.full_name
        Message.registry[self.full_name] = self
        if parent is None:
            Message.root_level_registry[self.full_name] = self
        self.options = MessageOptions(message.GetOptions(), message)
        if self.options.database:
            Message.database.append(self)
        if self.options.login:
            if Message.login_table is not None:
                raise RuntimeError('multiple login tables: {}, {}'.format(Message.login_table, self))
            Message.login_table = self
        self.fields = OrderedDict()
        for field_name, field in message.fields_by_name.items():
            self.fields[field_name] = Field(field, self)
        self.nested_messages = OrderedDict()
        for nested_name, nested in message.nested_types_by_name.items():
            self.nested_messages[nested_name] = Message(nested, package=package, parent=self)
        self.nested_enums = OrderedDict()
        for nested_name, nested in message.enum_types_by_name.items():
            self.nested_enums[nested_name] = Enum(nested, package=package, parent=self)
        self.py_src = None

    def set_src(self, py_src):
        self.py_src = py_src


class File(Meta):
    registry = OrderedDict()

    def __init__(self, file):
        self.descriptor = file
        self.name = file.name
        self.package = file.package
        File.registry[self.name] = self
        Package.item_registry.add(self.package)
        self.messages = OrderedDict()
        for message_name, message in file.message_types_by_name.items():
            self.messages[message_name] = Message(message, package=self.package)
        self.enums = OrderedDict()
        for enum_name, enum in file.enum_types_by_name.items():
            self.enums[enum_name] = Enum(enum, package=self.package)
        self.services = OrderedDict()
        for service_name, service in file.services_by_name.items():
            self.services[service_name] = Service(service, package=self.package)


def link():
    for message in Message.registry.values():
        for field in message.fields.values():
            if field.is_message():
                field.message_obj = Message.registry[field.message.full_name]
            if field.is_enum():
                field.enum_obj = Enum.registry[field.enum.full_name]
    for service in Service.registry.values():
        for method in service.methods.values():
            method.input_message = Message.registry[method.input_type.full_name]
            method.output_message = Message.registry[method.output_type.full_name]