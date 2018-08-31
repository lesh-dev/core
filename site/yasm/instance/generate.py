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
                    models[m].append((scl(tablename), CC(tablename) + "List", columnname, fk._column_tokens[2]))
                    models[tablename].append((columnname + "_fk", CC(m), m, fk._column_tokens[2]))

    def gen_interfaces():
        ts_interfaces = open("instance/ui/src/js/generated/interfaces.ts", "w")
        for name, fields in models.items():
            ts_interfaces.write("export interface {name} {{\n".format(name=CC(name)))
            for field in fields:
                ts_interfaces.write("    {name}: {type},\n".format(name=field[0], type=field[1]))
            ts_interfaces.write("}\n\n")
            ts_interfaces.write(
                "export interface {name}List {{\n    values: {name}[],\n    length: number\n}}\n\n".format(
                    name=CC(name)))
        ts_interfaces.close()

    def gen_defaults():
        def get_default(f, s):
            if s == 'number':
                return '0'
            elif s == 'string':
                return '"{}"'.format(f)
            elif s.endswith('List'):
                return '{{values: [], length: 0}} as {f}'.format(f=s)
            else:
                return 'default_{f}'.format(f=s)
        ts_defaults = open("instance/ui/src/js/generated/defaults.ts", "w")
        ts_defaults.write("import {")
        for name, fields in models.items():
            ts_defaults.write(CC(name))
            ts_defaults.write(', ')
            ts_defaults.write(CC(name) + 'List')
            ts_defaults.write(', ')
        ts_defaults.write('} from "./interfaces"\n\n')
        for name, fields in models.items():
            ts_defaults.write("export const default_{name} = {{\n".format(name=CC(name)))
            for field in fields:
                ts_defaults.write("    {name}: {type},\n".format(name=field[0], type=get_default(field[0], field[1])))
            ts_defaults.write("}} as {name};\n\n".format(name=CC(name)))
        ts_defaults.close()

    def gen_connectors():
        ts_connector = open("instance/ui/src/js/generated/api_connect.ts", "w")
        ts_connector.write("import {\n")
        for name, fields in models.items():
            ts_connector.write("    {name},\n    {name}List,\n".format(name=CC(name)))
        ts_connector.write("} from './interfaces'\n")
        ts_connector.write(connector_template)
        for name, fields in models.items():
            ts_connector.write("export function {name}_list(d: dict = {{}}) {{\n".format(name=name))
            ts_connector.write("    let req = '?';\n")
            ts_connector.write("    for (let key in d) {\n")
            ts_connector.write("        req += key + '=' + d[key] + '&'\n")
            ts_connector.write("    }\n")
            ts_connector.write("    return getRequest('/api/{name}_list' + req)\n}}\n\n\n".format(name=name))
            ts_connector.write("export function {name}_fill(obj: {type}) {{\n".format(name=name, type=CC(name)))
            ts_connector.write("    return new Promise<{type}>((resolve, reject) => {{\n".format(type=CC(name)))
            ts_connector.write("        let ans: {type} = obj;\n".format(type=CC(name)))
            ts_connector.write("        Promise.all([\n")
            for field in fields:
                if field[1].endswith("List"):
                    ts_connector.write("                {field}({{{filter}: String(obj.{value})}}),\n".format(field=field[0], filter=field[2], value=field[3]))
            ts_connector.write("             ]\n")
            ts_connector.write("        ).then((values) => {\n")
            n = 0
            for field in fields:
                if field[1].endswith("List"):
                    ts_connector.write("            ans.{field} = values[{n}];\n".format(field=field[0], n=n))
                    n += 1
            ts_connector.write("            resolve(ans);\n")
            ts_connector.write("        }).catch((error) => {\n")
            ts_connector.write("            reject(error);\n")
            ts_connector.write("        })\n")
            ts_connector.write("    })\n")
            ts_connector.write("}\n\n\n")
        ts_connector.close()

    def gen_api():
        read_api = open(previx + "/__init__.py", "w")
        read_api.write(api_imports)
        for name, fields in models.items():
            regular_fields = []
            additional_fields = []
            joined_fields = []
            for field in fields:
                if field[1] in MIME.values():
                    regular_fields.append(field[0])
                elif not field[1].endswith("List"):
                    joined_fields.append(field)
                else:
                    additional_fields.append(field[0])

            read_api.write("@module.route(\"/{name}\", methods=['GET'])\n".format(name=scl(name)))
            read_api.write("def {name}(req=None, raw=False):\n".format(name=scl(name)))
            read_api.write("    regular = [\n")
            for field in regular_fields:
                read_api.write("        '{}',\n".format(field))
            read_api.write("    ]\n")
            read_api.write("    additional = {\n")
            for field in additional_fields:
                read_api.write("        '{}': {{'length': 0, 'values': []}},\n".format(field))
            read_api.write("    }\n")
            read_api.write("    field = {\n")
            for field in regular_fields:
                read_api.write("        '{field}': {model}.{field},\n".format(field=field, model=name_2_model[name]))
            read_api.write("    }\n")
            read_api.write("    query = {model}.query\n".format(model=name_2_model[name]))
            read_api.write("    col = request.args.items() if req is None else req.items()\n")
            read_api.write("    for arg, val in col:\n")
            read_api.write("        if arg in regular:\n")
            read_api.write("            query = query.filter(field[arg] == val)\n".format(model=name_2_model[name]))
            read_api.write("    query = query.all()\n")
            read_api.write("    ans = []\n")
            read_api.write("    for entry in query:\n")
            read_api.write("        d = dict()\n")
            for field in joined_fields:
                read_api.write(
                    "        d['{field_name}'] = {func}(req={{'{field}': entry.{val}}}, raw=True)['values']\n".format(
                        field_name=field[0],
                        func=scl(field[2]),
                        field=field[3],
                        val=field[0][:-3]
                    ))
                read_api.write(
                    "        d['{field_name}'] = d['{field_name}'][0] if len(d['{field_name}']) else None\n".format(
                        field_name=field[0]))
            read_api.write("        d.update(entry.__dict__)\n")
            read_api.write("        d.pop('_sa_instance_state')\n")
            read_api.write("        d.update(additional)\n")
            read_api.write("        ans.append(d)\n")
            read_api.write("    if raw:\n")
            read_api.write("        return {\n")
            read_api.write("            'length': len(ans),\n")
            read_api.write("            'values': ans\n")
            read_api.write("        }\n")
            read_api.write("    return jsonify({\n")
            read_api.write("        'length': len(ans),\n")
            read_api.write("        'values': ans\n")
            read_api.write("    })\n\n\n")
        read_api.close()

    gen_interfaces()
    gen_connectors()
    gen_api()
    gen_defaults()


if __name__ == '__main__':
    main()
