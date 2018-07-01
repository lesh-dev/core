from flask import Flask
from .database import db


def create():
    yasm = Flask(__name__, instance_relative_config=True)
    yasm.config.from_object('config')
    yasm.config.from_pyfile('config.py')
    db.init_app(yasm)
    with yasm.test_request_context():
        db.create_all()

    import instance.public as pub
    yasm.register_blueprint(pub.module)
    import instance.admin as adm
    yasm.register_blueprint(adm.module)
    import instance.api as api
    yasm.register_blueprint(api.module)

    return yasm