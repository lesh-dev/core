from instance.database import db
from collections import OrderedDict
import os
import datetime

MIME = {
    int: "number",
    str: "string",
    datetime.date: "Date",
    datetime.datetime: "number",
    bytes: "string",
}


def CC(j):
    return "".join([x.title() for x in j.split("_")])


previx = "instance/api/generated"

api_imports = """from flask import Blueprint, jsonify, request
import instance.database
from flask_login import login_required
from instance.rights_decorator import has_rights

module = Blueprint('api', __name__, url_prefix='/api')


"""

connector_template = """
import {Promise} from 'es6-promise';

export function getRequest(url: string, type: string = 'GET'): Promise<any> {
    return new Promise<any>(
        function (resolve, reject) {
            const request = new XMLHttpRequest();
            request.onload = function () {
                if (this.status === 200) {
                    resolve(JSON.parse(this.response));
                } else {
                    reject(new Error(this.statusText));
                }
            };
            request.onerror = function () {
                reject(new Error('XMLHttpRequest Error: ' + this.statusText));
            };
            request.open(type, url);
            request.send();
        }
    );
}


export interface dict {
    [index: string]: string
}



"""

name_2_model = dict()
for model_name, model in db.Model._decl_class_registry.items():
    if hasattr(model, "__tablename__"):
        name_2_model[model.__tablename__] = model_name


def scl(name):
    return name


def main():  # NOQA
    if not os.path.exists(previx):
        os.mkdir(previx, 0o755)

    models = OrderedDict()

    for tablename, info in db.metadata.tables.items():
        models[tablename] = []
        for columnname, column in info._columns._data.items():

            models[tablename].append((columnname, MIME[column.type.python_type]))
            if len(column.foreign_keys):
                for fk in column.foreign_keys:
                    m = fk._column_tokens[1]
                    # models[m].append((scl(tablename), CC(tablename) + "[]", columnname, fk._column_tokens[2]))
                    for field_name, table in fk.referenced_model.relationships._data.items():
                        if table.table.name == tablename:
                            models[m].append((field_name, CC(tablename) + '[]', fk._column_tokens[2]))
                    try:
                        backref = list(
                            [
                                x[1].back_populates for x in
                                fk.referenced_model.relationships._data.items() if
                                list(list(x[1]._calculated_foreign_keys)[0].foreign_keys)[0] == fk
                            ]
                        )[0]
                    except Exception as e:
                        print(e)
                    models[tablename].append((backref, CC(m), m, fk._column_tokens[2]))

    def gen_interfaces():
        ts_interfaces = open("instance/ui/src/js/generated/interfaces.ts", "w")
        for name, fields in models.items():
            ts_interfaces.write("export interface {name} {{\n".format(name=CC(name)))
            for field in fields:
                ts_interfaces.write("    {name}: {type},\n".format(name=field[0], type=field[1]))
            ts_interfaces.write("}\n\n")
            # ts_interfaces.write(
            #     "export interface {name}List {{\n    values: {name}[],\n    length: number\n}}\n\n".format(
            #         name=CC(name)))
        ts_interfaces.close()

    def gen_defaults():
        def get_default(f, s):
            if s == 'number':
                return '0'
            elif s == 'string':
                return '"{}"'.format(f)
            elif s.endswith('[]'):
                return '[] as {f}'.format(f=s)
            elif s == 'Date':
                return 'new Date()'
            else:
                return 'default_{f}'.format(f=s)
        ts_defaults = open("instance/ui/src/js/generated/defaults.ts", "w")
        ts_defaults.write("import {")
        for name, fields in models.items():
            ts_defaults.write(CC(name))
            ts_defaults.write(', ')
        ts_defaults.write('} from "./interfaces"\n\n')
        for name, fields in models.items():
            ts_defaults.write("export var default_{name}: {name};\n".format(name=CC(name)))
        ts_defaults.write('\n\n')
        for name, fields in models.items():
            ts_defaults.write("default_{name} = {{\n".format(name=CC(name)))
            for field in fields:
                ts_defaults.write("    {name}: {type},\n".format(name=field[0], type=get_default(field[0], field[1])))
            ts_defaults.write("}};\n\n".format(name=CC(name)))
        ts_defaults.close()

    gen_interfaces()
    gen_defaults()


if __name__ == '__main__':
    main()
