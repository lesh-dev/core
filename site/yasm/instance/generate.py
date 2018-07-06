from instance.database import *
from collections import OrderedDict
import os

MIME = {
    int: "number",
    str: "string"
}


def CC(j):
    return "".join([x.title() for x in j.split("_")])


previx = "instance/api/generated"

api_imports = """from flask import Blueprint, jsonify, request
from instance.database import *

module = Blueprint('api', __name__, url_prefix='/api')


"""

connector_template = """
import {Promise} from 'es6-promise';

function getRequest(url: string): Promise<any> {
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
            request.open('GET', url);
            request.send();
        }
    );
}


"""

name_2_model = dict()
for model_name, model in db.Model._decl_class_registry.items():
    if hasattr(model, "__tablename__"):
        name_2_model[model.__tablename__] = model_name


def scl(name):
    return name + "_list"


def main():
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
                    models[m].append((scl(tablename), CC(tablename) + "List"))
                    models[tablename].append((m, CC(m)))

    ts_interfaces = open("instance/ui/src/js/generated/interfaces.ts", "w")
    for name, fields in models.items():
        ts_interfaces.write("export interface {name} {{\n".format(name=CC(name)))
        for field in fields:
            ts_interfaces.write("    {name}: {type},\n".format(name=field[0], type=field[1]))
        ts_interfaces.write("}\n\n")
        ts_interfaces.write("export interface {name}List {{\n    values: {name}[],\n    length: number\n}}\n\n".format(name=CC(name)))
    ts_interfaces.close()

    ts_connector = open("instance/ui/src/js/generated/api_connect.ts", "w")
    ts_connector.write("import {\n")
    for name, fields in models.items():
        ts_connector.write("    {name},\n    {name}List,\n".format(name=CC(name)))
    ts_connector.write("} from './interfaces'\n")
    ts_connector.write(connector_template)

    for name, fields in models.items():
        ts_connector.write("export function {name}_list() {{\n".format(name=name))
        ts_connector.write("    return getRequest('/api/{name}_list')\n}}\n\n\n".format(name=name))
        regular_fields = []
        additional_fields = []
        for field in fields:
            if field[1] in MIME.values():
                regular_fields.append(field[0])
            else:
                additional_fields.append(field[0])

    ts_connector.close()

    read_api = open(previx + "/__init__.py", "w")
    read_api.write(api_imports)
    for name, fields in models.items():
        regular_fields = []
        additional_fields = []
        for field in fields:
            if field[1] in MIME.values():
                regular_fields.append(field[0])
            else:
                additional_fields.append(field[0])

        read_api.write("@module.route(\"/{name}\", methods=['GET'])\n".format(name=scl(name)))
        read_api.write("def {name}():\n".format(name=scl(name)))
        read_api.write("    regular = [\n")
        for field in regular_fields:
            read_api.write("        '{}',\n".format(field))
        read_api.write("    ]\n")
        read_api.write("    additional = {\n")
        for field in additional_fields:
            read_api.write("        '{}': [],\n".format(field))
        read_api.write("    }\n")
        read_api.write("    field = {\n")
        for field in regular_fields:
            read_api.write("        '{field}': {model}.{field},\n".format(field=field, model=name_2_model[name]))
        read_api.write("    }\n")
        read_api.write("    query = {model}.query\n".format(model=name_2_model[name]))
        read_api.write("    for arg, val in request.args.items():\n")
        read_api.write("        if arg in regular:\n")
        read_api.write("            query = query.filter(field[arg] == val)\n".format(model=name_2_model[name]))
        read_api.write("    query = query.all()\n")
        read_api.write("    ans = []\n")
        read_api.write("    for entry in query:\n")
        read_api.write("        d = dict()\n")
        for field in regular_fields:
            read_api.write("        d['{field}'] = entry.{field}\n".format(field=field))
        read_api.write("        d.update(additional)\n")
        read_api.write("        ans.append(d)\n")
        read_api.write("    return jsonify({\n")
        read_api.write("        'length': len(ans),")
        read_api.write("        'values': ans")
        read_api.write("    })\n\n\n")
    read_api.close()


if __name__ == '__main__':
    main()
