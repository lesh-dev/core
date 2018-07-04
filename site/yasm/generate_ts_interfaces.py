from instance.database import db

MIME = {
    int: "number",
    str: "string"
}

def main():
    for tablename, info in db.metadata.tables.items():
        print("export interface {name}".format(name="".join([x.title() for x in tablename.split("_")])), "{")
        for colomnname, column in info._columns._data.items():
            print("    {name}: {type},".format(name=colomnname, type=MIME[column.type.python_type]))
        print("}")


if __name__ == '__main__':
    main()