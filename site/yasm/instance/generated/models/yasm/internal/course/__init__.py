import json
import sqlalchemy
import datetime
from flask_login import UserMixin

from .... import stub
from .... import yasm
from ..... import enums



class PatchTeachersRequest:
    def __init__(
        self,
        course_id=None,
        teachers=None,
    ):
        self.serialized = False
        if course_id is not None:
            assert isinstance(course_id, int)
            self.course_id = course_id
        if teachers is not None:
            assert isinstance(teachers, list)
            self.teachers = teachers


    @classmethod
    def from_json(cls, json_data):
        return cls(
            course_id=int(json_data['course_id']) if 'course_id' in json_data else None,
            teachers=[yasm.yasm.database.Person.from_json(item) for item in json_data.get('teachers', [])],
        )

    @classmethod
    def from_string(cls, data):
        return cls.from_json(json.loads(data))

    def to_json(self):
        self.serialized = True
        ret = dict()

        if isinstance(self.course_id, int):
            ret['course_id'] = self.course_id
        if  isinstance(self.teachers, list):
            ret['teachers'] = [value.to_json() for value in self.teachers if not value.serialized]
        self.serialized = False
        return ret

    def to_string(self):
        return json.dumps(self.to_json())




