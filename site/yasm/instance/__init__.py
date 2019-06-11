"""
.. _instance:
"""

from flask import Flask
from flask_wtf.csrf import CSRFProtect

from instance.database import db
from instance.login import lm
from instance.login.oauth2.base import Auth


def create():
    """
    .. _instance_create:

    Factory of flask applications, creates YaSM application.

    * creates flask app
    * initializes :ref:`database <database>`
    * initializes :ref:`login manager <login>`
    * populates it with all blueprints

    :return: Flask object
    """
    yasm = Flask(__name__, instance_relative_config=True)
    yasm.config.from_object('config')
    yasm.config.from_pyfile('config.py')
    csrf = CSRFProtect(yasm)
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
    import instance.secure_static as secure_static
    yasm.register_blueprint(secure_static.module)
    import instance.postgrest as postgrest
    yasm.register_blueprint(postgrest.module)
    import instance.docs as docs
    yasm.register_blueprint(docs.module)
    return yasm
