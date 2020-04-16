import json
import sqlalchemy
import datetime
from flask_login import UserMixin

from .. import stub
from .. import yasm
from ... import enums


class SearchRequest:
    def __init__(
        self,
        query=None,
        tables=None,
    ):
        self.serialized = False
        if query is not None:
            assert isinstance(query, str)
            self.query = query
        if tables is not None:
            assert isinstance(tables, list)
            self.tables = tables


    @classmethod
    def from_json(cls, json_data):
        return cls(
            query=str(json_data['query']) if 'query' in json_data else None,
            tables=[str(item) for item in json_data.get('tables', [])],
        )

    @classmethod
    def from_string(cls, data):
        return cls.from_json(json.loads(data))

    def to_json(self):
        self.serialized = True
        ret = dict()

        if isinstance(self.query, str):
            ret['query'] = self.query
        if  isinstance(self.tables, list):
            ret['tables'] = [value for value in self.tables ]
        self.serialized = False
        return ret

    def to_string(self):
        return json.dumps(self.to_json())


class SearchResponse:
    def __init__(
        self,
        query=None,
        person=None,
        department=None,
        school=None,
        course=None,
    ):
        self.serialized = False
        if query is not None:
            assert isinstance(query, str)
            self.query = query
        if person is not None:
            assert isinstance(person, list)
            self.person = person
        if department is not None:
            assert isinstance(department, list)
            self.department = department
        if school is not None:
            assert isinstance(school, list)
            self.school = school
        if course is not None:
            assert isinstance(course, list)
            self.course = course


    @classmethod
    def from_json(cls, json_data):
        return cls(
            query=str(json_data['query']) if 'query' in json_data else None,
            person=[yasm.yasm.database.Person.from_json(item) for item in json_data.get('person', [])],
            department=[yasm.yasm.database.Department.from_json(item) for item in json_data.get('department', [])],
            school=[yasm.yasm.database.School.from_json(item) for item in json_data.get('school', [])],
            course=[yasm.yasm.database.Course.from_json(item) for item in json_data.get('course', [])],
        )

    @classmethod
    def from_string(cls, data):
        return cls.from_json(json.loads(data))

    def to_json(self):
        self.serialized = True
        ret = dict()

        if isinstance(self.query, str):
            ret['query'] = self.query
        if  isinstance(self.person, list):
            ret['person'] = [value.to_json() for value in self.person if not value.serialized]
        if  isinstance(self.department, list):
            ret['department'] = [value.to_json() for value in self.department if not value.serialized]
        if  isinstance(self.school, list):
            ret['school'] = [value.to_json() for value in self.school if not value.serialized]
        if  isinstance(self.course, list):
            ret['course'] = [value.to_json() for value in self.course if not value.serialized]
        self.serialized = False
        return ret

    def to_string(self):
        return json.dumps(self.to_json())


