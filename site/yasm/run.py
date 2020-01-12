"""

"""

from instance import create
from flask_script import Manager

application = create()


def main():
    manager = Manager(application)
    manager.run()


if __name__ == '__main__':
    main()
