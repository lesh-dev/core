from flask import Flask
from .database import db
from .login import lm
from .login.oauth2.base import Auth

def create():
    yasm = Flask(__name__, instance_relative_config=True)
    yasm.config.from_object('config')
    yasm.config.from_pyfile('config.py')
    db.init_app(yasm)
    lm.init_app(yasm)
    Auth.init_app(yasm)
    with yasm.test_request_context():
        db.create_all()

    import instance.public as pub
    yasm.register_blueprint(pub.module)
    import instance.admin as adm
    yasm.register_blueprint(adm.module)
    import instance.api as api
    yasm.register_blueprint(api.module)
    import instance.react_components as react_components
    yasm.register_blueprint(react_components.module)
    import instance.login as login
    yasm.register_blueprint(login.module)
    import instance.personal as personal
    yasm.register_blueprint(personal.module)
    import instance.qr as qr
    yasm.register_blueprint(qr.module)
    return yasm
