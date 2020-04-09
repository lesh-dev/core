import json
import sqlalchemy
import datetime
from flask_login import UserMixin

from .... import stub
from .... import yasm
from ..... import enums


class FetchCourseRequest:
    def __init__(
        self,
        id=None,
    ):
        self.serialized = False
        if id is not None:
            assert isinstance(id, int)
            self.id = id


    @classmethod
    def from_json(cls, json_data):
        return cls(
            id=int(json_data['id']) if 'id' in json_data else None,
        )

    @classmethod
    def from_string(cls, data):
        return cls.from_json(json.loads(data))

    def to_json(self):
        self.serialized = True
        ret = dict()

        if isinstance(self.id, int):
            ret['id'] = self.id
        self.serialized = False
        return ret

    def to_string(self):
        return json.dumps(self.to_json())


class PatchTeachersRequest:
    def __init__(
        self,
        id=None,
        patch=None,
    ):
        self.serialized = False
        if id is not None:
            assert isinstance(id, int)
            self.id = id
        if patch is not None:
            assert isinstance(patch, dict)
            self.patch = patch


    @classmethod
    def from_json(cls, json_data):
        return cls(
            id=int(json_data['id']) if 'id' in json_data else None,
            patch={int(key): yasm.yasm.internal.course.TeachersPatchEntry.from_json(value) for key, value in json_data['patch'].items()} if 'patch' in json_data else None,
        )

    @classmethod
    def from_string(cls, data):
        return cls.from_json(json.loads(data))

    def to_json(self):
        self.serialized = True
        ret = dict()

        if isinstance(self.id, int):
            ret['id'] = self.id
        if  isinstance(self.patch, dict):
            ret['patch'] = {key: self.value.to_json() for key, value in self.patch}
        self.serialized = False
        return ret

    def to_string(self):
        return json.dumps(self.to_json())


class PatchTeachersResponse:
    def __init__(
        self,
        teachers=None,
    ):
        self.serialized = False
        if teachers is not None:
            assert isinstance(teachers, list)
            self.teachers = teachers


    @classmethod
    def from_json(cls, json_data):
        return cls(
            teachers=[yasm.yasm.database.Person.from_json(item) for item in json_data.get('teachers', [])],
        )

    @classmethod
    def from_string(cls, data):
        return cls.from_json(json.loads(data))

    def to_json(self):
        self.serialized = True
        ret = dict()

        if  isinstance(self.teachers, list):
            ret['teachers'] = [value.to_json() for value in self.teachers if not value.serialized]
        self.serialized = False
        return ret

    def to_string(self):
        return json.dumps(self.to_json())


class TeachersPatchEntry:
    def __init__(
        self,
        name=None,
        action=None,
    ):
        self.serialized = False
        if name is not None:
            assert isinstance(name, str)
            self.name = name
        if action is not None:
            assert isinstance(action, enums.yasm.internal.course.TeachersPatchActions)
            self.action = action


    @classmethod
    def from_json(cls, json_data):
        return cls(
            name=str(json_data['name']) if 'name' in json_data else None,
            action=enums.yasm.internal.course.TeachersPatchActions(json_data['action']) if 'action' in json_data else None,
        )

    @classmethod
    def from_string(cls, data):
        return cls.from_json(json.loads(data))

    def to_json(self):
        self.serialized = True
        ret = dict()

        if isinstance(self.name, str):
            ret['name'] = self.name
        if isinstance(self.action, enums.yasm.internal.course.TeachersPatchActions):
            ret['action'] = self.action.value
        self.serialized = False
        return ret

    def to_string(self):
        return json.dumps(self.to_json())


