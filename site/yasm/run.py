from flask import Flask
from instance import create
from flask_script import Manager


def main():
    app = create()
    manager = Manager(app)
    manager.run()


if __name__ == '__main__':
    main()
