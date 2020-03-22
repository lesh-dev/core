"""
.. _instance:
"""

from flask import Flask
from flask_wtf.csrf import CSRFProtect

from instance.generated.models.stub import db
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

    from instance.internal.people import APIPeople
    from instance.internal.course import APICourse
    from instance.internal.personal import APIPersonal
    from instance.builtins import APIBuiltin

    APICourse()
    APIPersonal()
    APIPeople()
    APIBuiltin()

    from instance.internal import module as internal
    yasm.register_blueprint(internal)

    from instance.public import module as pub
    from instance.react_components import module as react_components
    from instance.docs import module as docs
    from instance.postgrest import module as postgrest
    from instance.login import module as login

    yasm.register_blueprint(pub)
    yasm.register_blueprint(react_components)
    yasm.register_blueprint(docs)
    yasm.register_blueprint(postgrest)
    yasm.register_blueprint(login)

    from instance.generated.api import module as proto_api
    yasm.register_blueprint(proto_api)
    return yasm
