from google.protobuf.descriptor import FieldDescriptor
from collections import OrderedDict, defaultdict
import inflection


class AutogenOptions:
    class Database:
        db_table = None
        login_table = None
        table_name = None

        fk_name = None
        primary_key = None
        back_populates = None
        field_name = None
        searchable = None
        lazy_load = None
        nullable = None
        autoincrement = None

        enum_name = None
        enum_empty = None
        enum_pg_name = None

        @staticmethod
        def load(module):
            AutogenOptions.Database.db_table = module.db_table
            AutogenOptions.Database.login_table = module.login_table
            AutogenOptions.Database.table_name = module.table_name

            AutogenOptions.Database.primary_key = module.primary_key
            AutogenOptions.Database.back_populates = module.back_populates
            AutogenOptions.Database.field_name = module.field_name
            AutogenOptions.Database.searchable = module.searchable
            AutogenOptions.Database.lazy_load = module.lazy_load
            AutogenOptions.Database.nullable = module.nullable
            AutogenOptions.Database.autoincrement = module.autoincrement

            AutogenOptions.Database.enum_name = module.enum_name
            AutogenOptions.Database.enum_empty = module.enum_empty
            AutogenOptions.Database.enum_pg_name = module.enum_pg_name

    class API:
        service_require_login = None
        service_before_request = None
        service_personalized = None
        method_require_login = None
        method_before_request = None
        method_personalized = None


        @staticmethod
        def load(module):
            AutogenOptions.API.service_require_login = module.service_require_login
            AutogenOptions.API.service_before_request = module.service_before_request
            AutogenOptions.API.service_personalized = module.service_personalized
            AutogenOptions.API.method_require_login = module.method_require_login
            AutogenOptions.API.method_before_request = module.method_before_request
            AutogenOptions.API.method_personalized = module.method_personalized

    class Types:
        db_type = None
        py_type = None
        ts_type = None
        
        @staticmethod
        def load(module):
            AutogenOptions.Types.db_type = module.db_type
            AutogenOptions.Types.py_type = module.py_type
            AutogenOptions.Types.ts_type = module.ts_type


before_handlers = set()


class Meta:
    @property
    def is_internal(self):
        return self.full_name.startswith('yasm.lib')

    def __repr__(self):
        return f'{self.__class__.__name__}--{self.full_name or ""}'

    __str__ = __repr__

    def __hash__(self):
        return hash(self.full_name)


class Package:
    service_registry = set()
    item_registry = set()

    @classmethod
    def clear_registry(cls):
        cls.service_registry = set()
        cls.item_registry = set()


class MethodOptions:
    def __init__(self, options):
        self.descriptor = options
        self.require_login = options.Extensions[AutogenOptions.API.method_require_login]
        self.before_request = options.Extensions[AutogenOptions.API.method_before_request]
        self.personalized = options.Extensions[AutogenOptions.API.method_personalized]
        before_handlers.update(self.before_request)


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
        self.options = MethodOptions(method.GetOptions())
        self.additional_args = []
        if service.options.personalized:
            self.additional_args.append('current_user')

    @property
    def python_name(self):
        return inflection.underscore(self.name)


class ServiceOptions:
    def __init__(self, options):
        self.descriptor = options
        self.require_login = options.Extensions[AutogenOptions.API.service_require_login]
        self.before_request = options.Extensions[AutogenOptions.API.service_before_request]
        self.personalized = options.Extensions[AutogenOptions.API.service_personalized]
        before_handlers.update(self.before_request)


class Service(Meta):
    registry = OrderedDict()

    @classmethod
    def clear_registry(cls):
        cls.registry = OrderedDict()

    def __init__(self, service, file):
        self.descriptor = service
        self.name = service.name
        self.package = file.package
        self.options = ServiceOptions(service.GetOptions())
        self.file = file
        Package.service_registry.add(file.package)
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
        value_name = value.GetOptions().Extensions[AutogenOptions.Database.enum_name]
        if value_name:
            self.name = value_name
        self.value = self.name if not value.GetOptions().Extensions[AutogenOptions.Database.enum_empty] else ""


class Enum(Meta):
    registry = OrderedDict()
    root_level_registry = OrderedDict()

    @classmethod
    def clear_registry(cls):
        cls.registry = OrderedDict()
        cls.root_level_registry = OrderedDict()

    def __init__(self, enum, package, parent=None):
        self.descriptor = enum
        self.name = enum.name
        self.package = package
        Package.item_registry.add(package)
        self.parent = parent
        self.full_name = enum.full_name
        self.pg_name = enum.GetOptions().Extensions[AutogenOptions.Database.enum_pg_name]
        if parent is None:
            Enum.root_level_registry[self.full_name] = self
        Enum.registry[self.full_name] = self
        self.values = OrderedDict()
        for value_name, value in enum.values_by_name.items():
            self.values[value_name] = Value(value)


class FieldOptions:
    def __init__(self, options):
        self.primary_key = options.Extensions[AutogenOptions.Database.primary_key]
        self.back_populates = options.Extensions[AutogenOptions.Database.back_populates]
        self.field_name = options.Extensions[AutogenOptions.Database.field_name]
        self.searchable = options.Extensions[AutogenOptions.Database.searchable]
        self.lazy_load = options.Extensions[AutogenOptions.Database.lazy_load]
        self.nullable = options.Extensions[AutogenOptions.Database.nullable]
        self.autoincrement = options.Extensions[AutogenOptions.Database.autoincrement]


class Field(Meta):
    def __init__(self, field, message):
        self.descriptor = field
        self.name = field.name
        self.full_name = field.full_name
        self.number = field.number
        self.label = field.label
        self.type = field.type
        self.label = field.label
        self.repeated = self.label == FieldDescriptor.LABEL_REPEATED
        self.message = None
        self.back_populates = None
        self.package = message.package
        if field.message_type is not None:
            self.message = field.message_type
        self.enum = None
        if field.enum_type is not None:
            self.enum = field.enum_type
        self.message_obj = None
        self.enum_obj = None
        self.options = FieldOptions(field.GetOptions())
        if not message.options.db_table:
            if self.options.primary_key or self.options.lazy_load:
                raise RuntimeError('database options in {} of {}, which is not a db_table'.format(self, message))
        if self.options.searchable:
            message.options.searchable = True

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
        if self.repeated:
            repeated = '[]'
        if self.is_enum():
            return f'interfaces.{self.enum.full_name}{repeated}'
        if self.is_message():
            if not self.message_obj.options.ts_type:
                if self.message_obj.options.map_entry:
                    key = None
                    value = None
                    for field in self.message_obj.fields.values():
                        if field.name == 'key':
                            key = field
                        if field.name == 'value':
                            value = field
                    return f'interfaces.{self.message_obj.full_name}'
                return f'interfaces.{self.message_obj.full_name}{repeated}'
            return self.message_obj.options.ts_type
        if self.type == FieldDescriptor.TYPE_BOOL:
            return f'boolean{repeated}'
        if self.type == FieldDescriptor.TYPE_STRING:
            return f'string{repeated}'
        return f'number{repeated}'

    @property
    def map_ts_type(self):
        key = None
        value = None
        for field in self.message_obj.fields.values():
            if field.name == 'key':
                key = field
            if field.name == 'value':
                value = field
        return f'{{[index: {key.ts_type}]: {value.ts_type}}}'

    @property
    def py_db_type(self):
        template = '{}'
        if self.label == FieldDescriptor.LABEL_REPEATED:
            template = 'ARRAY(db.{})'
        if self.is_enum():
            tp = f'Enum(*tuple(x.value for x in enums.{self.enum_obj.full_name}), name=\'{self.enum_obj.pg_name}\')'
        elif self.is_message():
            if not self.message_obj.options.db_type:
                tp = 'JSON'
            else:
                tp = self.message_obj.options.db_type
        elif self.type == FieldDescriptor.TYPE_STRING:
            tp = 'Text'
        elif self.type == FieldDescriptor.TYPE_BOOL:
            tp = 'Boolean'
        elif self.type in [
            FieldDescriptor.TYPE_FLOAT,
            FieldDescriptor.TYPE_DOUBLE,
        ]:
            tp = 'Float'
        else:
            tp = 'Integer'
        return template.format(tp)

    @property
    def py_type(self):
        if self.is_enum():
            return 'enums.{}'.format(self.enum_obj.full_name)
        elif self.is_message():
            if not self.is_system_type():
                return 'yasm.{}'.format(self.message_obj.full_name)
            else:
                return self.message_obj.options.py_type
        elif self.type == FieldDescriptor.TYPE_STRING:
            return 'str'
        elif self.type == FieldDescriptor.TYPE_BOOL:
            return 'bool'
        elif self.type in [
            FieldDescriptor.TYPE_FLOAT,
            FieldDescriptor.TYPE_DOUBLE,
        ]:
            return 'float'
        else:
            return 'int'

    @property
    def py_cast(self):
        if self.is_message():
            tp = self.py_type
            if not self.is_system_type():
                return tp + '.from_json'
            else:
                return tp
        return self.py_type

    def is_system_type(self):
        return bool(
            self.message_obj.options.py_type
            or self.message_obj.options.db_type
            or self.message_obj.options.ts_type
            # or self.message_obj.options.py_package
        )


class MessageOptions:
    def __init__(self, options, message):
        self.descriptor = options
        self.message = message
        self.map_entry = options.map_entry
        self.db_table = options.Extensions[AutogenOptions.Database.db_table]
        self.table_name = options.Extensions[AutogenOptions.Database.table_name]
        self.login = options.Extensions[AutogenOptions.Database.login_table]
        self.searchable = False
        self.db_type = options.Extensions[AutogenOptions.Types.db_type]
        self.py_type = options.Extensions[AutogenOptions.Types.py_type]
        self.ts_type = options.Extensions[AutogenOptions.Types.ts_type]


class Relationship():
    def __init__(self, name, model, fields, back_populates, repeated, back_repeated):
        self.fields = fields
        self.name = name
        self.model = model
        self.back_populates = back_populates
        self.repeated = repeated
        self.back_repeated = back_repeated


class Message(Meta):
    registry = OrderedDict()
    root_level_registry = OrderedDict()
    login_table = None
    map_for = None

    @classmethod
    def clear_registry(cls):
        cls.registry = OrderedDict()
        cls.root_level_registry = OrderedDict()
        cls.login_table = None

    def __init__(self, message, package, parent=None):
        self.descriptor = message
        self.name = message.name
        self.parent = parent
        self.package = package
        self.full_name = message.full_name
        self.table_name = None
        self.primary_fields = []
        self.regular_fields = []
        self.relationships = dict()
        self.back_refs = defaultdict(list)
        Message.registry[self.full_name] = self
        if parent is None:
            Message.root_level_registry[self.full_name] = self
        self.options = MessageOptions(message.GetOptions(), message)
        if self.options.db_table:
            if self.package != 'yasm.database':
                raise RuntimeError('db_table {} not in yasm.database package'.format(self))
        if self.options.login:
            if Message.login_table is not None:
                raise RuntimeError('multiple login tables: {}, {}'.format(Message.login_table, self))
            if self.options.db_table:
                Message.login_table = self
            else:
                raise RuntimeError('can not set non db_table as a login table {}'.format(self))
        if self.options.table_name:
            if not self.options.db_table:
                raise RuntimeError('cat not set table name for non db_table {}'.format(self))
        self.primary_keys = OrderedDict()
        self.regular_keys = OrderedDict()
        self.deps = set()
        self.enum_deps = []
        self.fields = OrderedDict()
        for field_name, field in message.fields_by_name.items():
            self.fields[field_name] = field = Field(field, self)
            if self.fields[field_name].options.primary_key:
                self.primary_keys[field_name] = field
            else:
                self.regular_keys[field_name] = field
        if self.options.db_table and len(self.primary_keys) == 0:
            raise RuntimeError(f'No primary key for {self}')
        if not self.options.table_name:
            self.table_name = self.name.lower()
        else:
            self.table_name = self.options.table_name
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

    @classmethod
    def clear_registry(cls):
        cls.registry = OrderedDict()

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
            self.services[service_name] = Service(service, file=self)


def dfs(entity, getter, used, out):
    used[entity] = 'GREY'
    for neighbour in getter(entity):
        if used[neighbour] == 'WHITE':
            dfs(neighbour, getter, used, out)
        elif used[neighbour] == 'GREY':
            raise RuntimeError(f'cycle on {entity}, {neighbour}, maybe more')
    out.append(entity)
    used[entity] = 'BLACK'


def cover_dfs(data, getter):
    used = {
        entity: 'WHITE'
        for entity in data
    }
    out = []
    for entity in data:
        if used[entity] == 'WHITE':
            dfs(entity, getter, used, out)
    return out


def get_back_populates(back_refs, key):
    back_populates = None
    if key.options.back_populates:
        for back_ref in back_refs:
            if back_ref.name == key.options.back_populates:
                back_populates = back_ref
    else:
        if len(back_refs) == 1:
            back_populates = back_refs[0]
    if back_populates is None:
        raise RuntimeError(f'can not find back ref for {key}')
    return back_populates


def link():
    # Object linking
    for message in Message.registry.values():
        for field in message.fields.values():
            if field.is_message():
                field.message_obj = Message.registry[field.message.full_name]
                if field.message_obj.options.map_entry:
                    field.message_obj.map_for = field
            if field.is_enum():
                field.enum_obj = Enum.registry[field.enum.full_name]
                if field.is_enum():
                    message.enum_deps.append(field.enum_obj)

    for message in Message.registry.values():
        if message.options.db_table:
            for primary_key in message.primary_keys.values():
                if primary_key.is_message() and primary_key.message_obj.options.db_table:
                    message.deps.add(primary_key.message_obj)

    # Field back_refs
    for message in Message.registry.values():
        if message.options.db_table:
            for field in message.fields.values():
                if field.is_message():
                    if field.message_obj.options.db_table:
                        for back in field.message_obj.fields.values():
                            if back.is_message() and back.message_obj.full_name == message.full_name:
                                message.back_refs[field].append(back)
                        if not message.back_refs[field]:
                            raise RuntimeError(f'can not find back_ref for {field} in {field.message_obj}')

    for message in cover_dfs(Message.registry.values(), lambda self: self.deps):
        if message.options.db_table:
            for key in message.primary_keys.values():
                if key.is_message() and key.message_obj.options.db_table:
                    if not key.repeated:
                        back_populates = get_back_populates(message.back_refs[key], key)
                        additional = []
                        if back_populates.repeated or key.options.primary_key:
                            for field in key.message_obj.primary_fields:
                                additional.append(Field(field.descriptor, message))
                                additional[-1].back_populates = additional[-1].options.field_name or additional[-1].name
                                additional[-1].options = key.options
                                additional[-1].name = f'fk_{key.message_obj.table_name}_{field.name}'
                            message.primary_fields.extend(additional)
                        if len(additional) == 1 and key.options.field_name:
                            additional[-1].options.field_name = key.options.field_name
                        message.relationships[key.name] = Relationship(
                            name=key.name,
                            model=key.message_obj,
                            fields=additional,
                            back_populates=back_populates,
                            repeated=False,
                            back_repeated=back_populates.repeated,
                        )
                    else:
                        raise RuntimeError(f'field {key} is repeated and primary')
                else:  # native
                    message.primary_fields.append(key)

    for message in Message.registry.values():
        if message.options.db_table:
            for key in message.regular_keys.values():
                if key.is_message() and key.message_obj.options.db_table:
                    back_populates = get_back_populates(message.back_refs[key], key)
                    if not key.repeated:
                        additional = []
                        if back_populates.repeated or not key.options.nullable:
                            if not key.repeated and not back_populates.repeated and not key.options.nullable and not back_populates.options.nullable:
                                raise RuntimeError(f'both {key} and {back_populates} are not nullable (at least one must be nullable)')
                            for field in key.message_obj.primary_fields:
                                additional.append(Field(field.descriptor, message))
                                additional[-1].name = f'fk_{key.name}_{field.name}'
                                additional[-1].options = key.options
                                additional[-1].back_populates = field.options.field_name or field.name
                            message.regular_fields.extend(additional)
                        if len(additional) == 1 and key.options.field_name:
                            additional[-1].options.field_name = key.options.field_name
                        message.relationships[key.name] = Relationship(
                            name=key.name,
                            model=key.message_obj,
                            fields=additional,
                            back_populates=back_populates,
                            repeated=False,
                            back_repeated=back_populates.repeated,
                        )
                    else:
                        message.relationships[key.name] = Relationship(
                            name=key.name,
                            model=key.message_obj,
                            fields=[],
                            back_populates=back_populates,
                            repeated=True,
                            back_repeated=back_populates.repeated,
                        )
                else:  # native
                    message.regular_fields.append(key)

    for service in Service.registry.values():
        for method in service.methods.values():
            method.input_message = Message.registry[method.input_type.full_name]
            method.output_message = Message.registry[method.output_type.full_name]
