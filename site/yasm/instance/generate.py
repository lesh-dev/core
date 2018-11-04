from instance.database import db
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
    return name + "_list"


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
                    models[m].append((scl(tablename), CC(tablename) + "List", columnname, fk._column_tokens[2]))
                    try:
                        backref = list(
                            map(
                                lambda x: x[1].back_populates,
                                filter(
                                    lambda i: list(list(i[1]._calculated_foreign_keys)[0].foreign_keys)[0] == fk,
                                    fk.referenced_model.relationships._data.items()
                                )
                            )
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
            ts_connector.write("    return getRequest('/api/{name}_list' + req) as Promise<{interface_name}List>\n}}\n\n\n".format(name=name, interface_name=CC(name)))  # NOQA
            ts_connector.write("export function {name}_fill(obj: {type}) {{\n".format(name=name, type=CC(name)))
            ts_connector.write("    return new Promise<{type}>((resolve, reject) => {{\n".format(type=CC(name)))
            ts_connector.write("        let ans: {type} = obj;\n".format(type=CC(name)))
            ts_connector.write("        Promise.all([\n")
            for field in fields:
                if field[1].endswith("List"):
                    ts_connector.write("                {field}({{{filter}: String(obj.{value})}}),\n".format(field=field[0], filter=field[2], value=field[3]))  # NOQA
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
        for i, (name, fields) in enumerate(models.items()):
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
            read_api.write("@has_rights('admin')\n")
            read_api.write("@login_required\n")
            read_api.write("def {name}(req=None):\n".format(name=scl(name)))
            read_api.write("    regular = [\n")
            for field in regular_fields:
                read_api.write("        '{}',\n".format(field))
            read_api.write("    ]\n")
            read_api.write("    field = {\n")
            for field in regular_fields:
                read_api.write("        '{field}': instance.database.{model}.{field},\n".format(
                    field=field,
                    model=name_2_model[name]
                ))
            read_api.write("    }\n")
            read_api.write("    query = instance.database.{model}.query\n".format(model=name_2_model[name]))
            read_api.write("    col = request.args.items() if req is None else req.items()\n")
            read_api.write("    for arg, val in col:\n")
            read_api.write("        if arg in regular:\n")
            read_api.write("            query = query.filter(field[arg] == val)\n".format(model=name_2_model[name]))
            read_api.write("    query = query.all()\n")
            read_api.write("    ans = []\n")
            read_api.write("    for entry in query:\n")
            read_api.write("        ans.append(entry.serialize())\n")
            read_api.write("    return jsonify({\n")
            read_api.write("        'length': len(ans),\n")
            read_api.write("        'values': ans\n")
            read_api.write("    })\n")
            if i + 1 < len(models):
                read_api.write("\n\n")
        read_api.close()

    def gen_backend_speedtests():
        tests = open('tests/TestSpeed/generated.py', 'w')
        tests.write('import unittest\n')
        tests.write('import timeit\n')
        tests.write('import sys\n')
        tests.write('import json\n')
        tests.write('import instance\n')
        tests.write('import instance.login.controllers\n')
        tests.write('from flask_login import login_user\n')
        tests.write('import tests.testinglib as testinglib\n')
        for name, fields in models.items():
            tests.write('from instance.api.generated import {name}\n'.format(name=scl(name)))
        tests.write('yasm = instance.create()\n\n\n')
        tests.write('class TestSpeed(unittest.TestCase):\n')
        for i, (name, fields) in enumerate(models.items()):
            tests.write('    @testinglib.load_result\n')
            tests.write('    @testinglib.request_needed(yasm)\n')
            tests.write('    @testinglib.login_needed(467)\n')
            tests.write('    def test_{name}(self):\n'.format(name=scl(name)))
            tests.write('        time = timeit.timeit({name}, number=10) / 10\n'.format(name=scl(name)))
            tests.write('        if testinglib.result.get():\n')
            tests.write('            assert testinglib.result.get() * 1.1 > time\n')
            tests.write('            if time < testinglib.result.get():\n')
            tests.write('                testinglib.result.set(time)\n')
            tests.write('        else:\n')
            tests.write('            testinglib.result.set(time)\n')
            if i + 1 < len(models):
                tests.write('\n')

    gen_interfaces()
    gen_connectors()
    gen_api()
    gen_defaults()
    gen_backend_speedtests()


if __name__ == '__main__':
    main()
