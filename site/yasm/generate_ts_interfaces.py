from instance.database import db

MIME = {
    int: "number",
    str: "string"
}

def CC(j):
    return "".join([x.title() for x in j.split("_")])

def main():
    for tablename, info in db.metadata.tables.items():
        print("export interface {name}".format(name=CC(tablename)), "{")
        for columnname, column in info._columns._data.items():
            print("    {name}: {type},".format(name=columnname, type=MIME[column.type.python_type]))
        print("}")
        print("export interface {name}List".format(name=CC(tablename)), "{")
        print("    [index: number]: {}".format(CC(tablename)))
        print('}')


if __name__ == '__main__':
    main()