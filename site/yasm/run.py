"""

"""

from instance import create
from instance.autogen.generate import main as proto_gen
from flask_script import Manager

application = create()


def main():
    manager = Manager(application)

    @manager.command
    def generate():
        """generate base classes/interfaces/handlers from proto-scheme"""
        proto_gen()

    manager.run()


if __name__ == '__main__':
    main()
