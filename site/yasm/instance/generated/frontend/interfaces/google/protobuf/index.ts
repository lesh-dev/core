import * as interfaces from '../../index'

export {

}


    export namespace Empty {
                    }
    export interface Empty {
            }


    export namespace FileDescriptorSet {
                    }
    export interface FileDescriptorSet {
                    file?: interfaces.google.protobuf.FileDescriptorProto[]
            }


    export namespace FileDescriptorProto {
                    }
    export interface FileDescriptorProto {
                    name?: string
                    package?: string
                    dependency?: string[]
                    public_dependency?: number[]
                    weak_dependency?: number[]
                    message_type?: interfaces.google.protobuf.DescriptorProto[]
                    enum_type?: interfaces.google.protobuf.EnumDescriptorProto[]
                    service?: interfaces.google.protobuf.ServiceDescriptorProto[]
                    extension?: interfaces.google.protobuf.FieldDescriptorProto[]
                    options?: interfaces.google.protobuf.FileOptions
                    source_code_info?: interfaces.google.protobuf.SourceCodeInfo
                    syntax?: string
            }


    export namespace DescriptorProto {
                                        export namespace ExtensionRange {
                    }
    export interface ExtensionRange {
                    start?: number
                    end?: number
                    options?: interfaces.google.protobuf.ExtensionRangeOptions
            }

                                                    export namespace ReservedRange {
                    }
    export interface ReservedRange {
                    start?: number
                    end?: number
            }

                                }
    export interface DescriptorProto {
                    name?: string
                    field?: interfaces.google.protobuf.FieldDescriptorProto[]
                    extension?: interfaces.google.protobuf.FieldDescriptorProto[]
                    nested_type?: interfaces.google.protobuf.DescriptorProto[]
                    enum_type?: interfaces.google.protobuf.EnumDescriptorProto[]
                    extension_range?: interfaces.google.protobuf.DescriptorProto.ExtensionRange[]
                    oneof_decl?: interfaces.google.protobuf.OneofDescriptorProto[]
                    options?: interfaces.google.protobuf.MessageOptions
                    reserved_range?: interfaces.google.protobuf.DescriptorProto.ReservedRange[]
                    reserved_name?: string[]
            }


    export namespace ExtensionRangeOptions {
                    }
    export interface ExtensionRangeOptions {
                    uninterpreted_option?: interfaces.google.protobuf.UninterpretedOption[]
            }


    export namespace FieldDescriptorProto {
                                export enum Type {
                    TYPE_DOUBLE = 'TYPE_DOUBLE',
                    TYPE_FLOAT = 'TYPE_FLOAT',
                    TYPE_INT64 = 'TYPE_INT64',
                    TYPE_UINT64 = 'TYPE_UINT64',
                    TYPE_INT32 = 'TYPE_INT32',
                    TYPE_FIXED64 = 'TYPE_FIXED64',
                    TYPE_FIXED32 = 'TYPE_FIXED32',
                    TYPE_BOOL = 'TYPE_BOOL',
                    TYPE_STRING = 'TYPE_STRING',
                    TYPE_GROUP = 'TYPE_GROUP',
                    TYPE_MESSAGE = 'TYPE_MESSAGE',
                    TYPE_BYTES = 'TYPE_BYTES',
                    TYPE_UINT32 = 'TYPE_UINT32',
                    TYPE_ENUM = 'TYPE_ENUM',
                    TYPE_SFIXED32 = 'TYPE_SFIXED32',
                    TYPE_SFIXED64 = 'TYPE_SFIXED64',
                    TYPE_SINT32 = 'TYPE_SINT32',
                    TYPE_SINT64 = 'TYPE_SINT64',
            }

                        export enum Label {
                    LABEL_OPTIONAL = 'LABEL_OPTIONAL',
                    LABEL_REQUIRED = 'LABEL_REQUIRED',
                    LABEL_REPEATED = 'LABEL_REPEATED',
            }

            }
    export interface FieldDescriptorProto {
                    name?: string
                    number?: number
                    label?: interfaces.google.protobuf.FieldDescriptorProto.Label
                    type?: interfaces.google.protobuf.FieldDescriptorProto.Type
                    type_name?: string
                    extendee?: string
                    default_value?: string
                    oneof_index?: number
                    json_name?: string
                    options?: interfaces.google.protobuf.FieldOptions
            }


    export namespace OneofDescriptorProto {
                    }
    export interface OneofDescriptorProto {
                    name?: string
                    options?: interfaces.google.protobuf.OneofOptions
            }


    export namespace EnumDescriptorProto {
                                        export namespace EnumReservedRange {
                    }
    export interface EnumReservedRange {
                    start?: number
                    end?: number
            }

                                }
    export interface EnumDescriptorProto {
                    name?: string
                    value?: interfaces.google.protobuf.EnumValueDescriptorProto[]
                    options?: interfaces.google.protobuf.EnumOptions
                    reserved_range?: interfaces.google.protobuf.EnumDescriptorProto.EnumReservedRange[]
                    reserved_name?: string[]
            }


    export namespace EnumValueDescriptorProto {
                    }
    export interface EnumValueDescriptorProto {
                    name?: string
                    number?: number
                    options?: interfaces.google.protobuf.EnumValueOptions
            }


    export namespace ServiceDescriptorProto {
                    }
    export interface ServiceDescriptorProto {
                    name?: string
                    method?: interfaces.google.protobuf.MethodDescriptorProto[]
                    options?: interfaces.google.protobuf.ServiceOptions
            }


    export namespace MethodDescriptorProto {
                    }
    export interface MethodDescriptorProto {
                    name?: string
                    input_type?: string
                    output_type?: string
                    options?: interfaces.google.protobuf.MethodOptions
                    client_streaming?: boolean
                    server_streaming?: boolean
            }


    export namespace FileOptions {
                                export enum OptimizeMode {
                    SPEED = 'SPEED',
                    CODE_SIZE = 'CODE_SIZE',
                    LITE_RUNTIME = 'LITE_RUNTIME',
            }

            }
    export interface FileOptions {
                    java_package?: string
                    java_outer_classname?: string
                    java_multiple_files?: boolean
                    java_generate_equals_and_hash?: boolean
                    java_string_check_utf8?: boolean
                    optimize_for?: interfaces.google.protobuf.FileOptions.OptimizeMode
                    go_package?: string
                    cc_generic_services?: boolean
                    java_generic_services?: boolean
                    py_generic_services?: boolean
                    php_generic_services?: boolean
                    deprecated?: boolean
                    cc_enable_arenas?: boolean
                    objc_class_prefix?: string
                    csharp_namespace?: string
                    swift_prefix?: string
                    php_class_prefix?: string
                    php_namespace?: string
                    php_metadata_namespace?: string
                    ruby_package?: string
                    uninterpreted_option?: interfaces.google.protobuf.UninterpretedOption[]
            }


    export namespace MessageOptions {
                    }
    export interface MessageOptions {
                    message_set_wire_format?: boolean
                    no_standard_descriptor_accessor?: boolean
                    deprecated?: boolean
                    map_entry?: boolean
                    uninterpreted_option?: interfaces.google.protobuf.UninterpretedOption[]
            }


    export namespace FieldOptions {
                                export enum CType {
                    STRING = 'STRING',
                    CORD = 'CORD',
                    STRING_PIECE = 'STRING_PIECE',
            }

                        export enum JSType {
                    JS_NORMAL = 'JS_NORMAL',
                    JS_STRING = 'JS_STRING',
                    JS_NUMBER = 'JS_NUMBER',
            }

            }
    export interface FieldOptions {
                    ctype?: interfaces.google.protobuf.FieldOptions.CType
                    packed?: boolean
                    jstype?: interfaces.google.protobuf.FieldOptions.JSType
                    lazy?: boolean
                    deprecated?: boolean
                    weak?: boolean
                    uninterpreted_option?: interfaces.google.protobuf.UninterpretedOption[]
            }


    export namespace OneofOptions {
                    }
    export interface OneofOptions {
                    uninterpreted_option?: interfaces.google.protobuf.UninterpretedOption[]
            }


    export namespace EnumOptions {
                    }
    export interface EnumOptions {
                    allow_alias?: boolean
                    deprecated?: boolean
                    uninterpreted_option?: interfaces.google.protobuf.UninterpretedOption[]
            }


    export namespace EnumValueOptions {
                    }
    export interface EnumValueOptions {
                    deprecated?: boolean
                    uninterpreted_option?: interfaces.google.protobuf.UninterpretedOption[]
            }


    export namespace ServiceOptions {
                    }
    export interface ServiceOptions {
                    deprecated?: boolean
                    uninterpreted_option?: interfaces.google.protobuf.UninterpretedOption[]
            }


    export namespace MethodOptions {
                                export enum IdempotencyLevel {
                    IDEMPOTENCY_UNKNOWN = 'IDEMPOTENCY_UNKNOWN',
                    NO_SIDE_EFFECTS = 'NO_SIDE_EFFECTS',
                    IDEMPOTENT = 'IDEMPOTENT',
            }

            }
    export interface MethodOptions {
                    deprecated?: boolean
                    idempotency_level?: interfaces.google.protobuf.MethodOptions.IdempotencyLevel
                    uninterpreted_option?: interfaces.google.protobuf.UninterpretedOption[]
            }


    export namespace UninterpretedOption {
                                        export namespace NamePart {
                    }
    export interface NamePart {
                    name_part?: string
                    is_extension?: boolean
            }

                                }
    export interface UninterpretedOption {
                    name?: interfaces.google.protobuf.UninterpretedOption.NamePart[]
                    identifier_value?: string
                    positive_int_value?: number
                    negative_int_value?: number
                    double_value?: number
                    string_value?: number
                    aggregate_value?: string
            }


    export namespace SourceCodeInfo {
                                        export namespace Location {
                    }
    export interface Location {
                    path?: number[]
                    span?: number[]
                    leading_comments?: string
                    trailing_comments?: string
                    leading_detached_comments?: string[]
            }

                                }
    export interface SourceCodeInfo {
                    location?: interfaces.google.protobuf.SourceCodeInfo.Location[]
            }


    export namespace GeneratedCodeInfo {
                                        export namespace Annotation {
                    }
    export interface Annotation {
                    path?: number[]
                    source_file?: string
                    begin?: number
                    end?: number
            }

                                }
    export interface GeneratedCodeInfo {
                    annotation?: interfaces.google.protobuf.GeneratedCodeInfo.Annotation[]
            }

