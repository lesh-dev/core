from flask import request
from flask_json import as_json
from flask.views import View

from db import Person, PersonSchool, School


class School2Persons(View):
    @as_json
    def dispatch_request(self, school_id):
        school = School.query.get(school_id)
        return {1 : 1}
