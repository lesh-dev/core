from flask import request
from sqlalchemy import or_
from flask.views import View
from flask_json import FlaskJSON, as_json
from json import loads
from checks import *
from marshmallow_jsonapi.flask import Schema
from marshmallow_jsonapi import fields
from flask_rest_jsonapi import ResourceDetail, ResourceList


class PersonSchema(Schema):  # only for DRY honor
    class Meta:
        type_ = 'person'
        self_view = 'person_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'person_list'

    id = fields.Integer(as_string=True, dump_only=True, attribute='person_id')
    first_name = fields.Str()
    last_name = fields.Str()


class PersonList(ResourceList):
    schema = PersonSchema
    data_layer = {
        'session': db.database.session,
        'model': db.Person
    }


class PersonDetail(ResourceDetail):
    schema = PersonSchema
    data_layer = {
        'session': db.database.session,
        'model': db.Person
    }
