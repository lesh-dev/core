import json
import sqlalchemy
import datetime
from flask_login import UserMixin

from .... import stub
from .... import yasm
from ..... import enums


class ContactList:
    def __init__(
        self,
        contacts=None,
    ):
        self.serialized = False
        if contacts is not None:
            assert isinstance(contacts, list)
            self.contacts = contacts


    @classmethod
    def from_json(cls, json_data):
        return cls(
            contacts=[yasm.yasm.database.Contact.from_json(item) for item in json_data.get('contacts', [])],
        )

    @classmethod
    def from_string(cls, data):
        return cls.from_json(json.loads(data))

    def to_json(self):
        self.serialized = True
        ret = dict()

        if  isinstance(self.contacts, list):
            ret['contacts'] = [value.to_json() for value in self.contacts if not value.serialized]
        self.serialized = False
        return ret

    def to_string(self):
        return json.dumps(self.to_json())


class ContactsPatch:
    def __init__(
        self,
        patch=None,
    ):
        self.serialized = False
        if patch is not None:
            assert isinstance(patch, dict)
            self.patch = patch


    @classmethod
    def from_json(cls, json_data):
        return cls(
            patch={str(key): yasm.yasm.internal.person.ContactsPatchEntry.from_json(value) for key, value in json_data['patch'].items()} if 'patch' in json_data else None,
        )

    @classmethod
    def from_string(cls, data):
        return cls.from_json(json.loads(data))

    def to_json(self):
        self.serialized = True
        ret = dict()

        if  isinstance(self.patch, dict):
            ret['patch'] = {key: self.value.to_json() for key, value in self.patch}
        self.serialized = False
        return ret

    def to_string(self):
        return json.dumps(self.to_json())


class ContactsPatchEntry:
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
            assert isinstance(action, enums.yasm.internal.person.ContactsPatchActions)
            self.action = action


    @classmethod
    def from_json(cls, json_data):
        return cls(
            name=str(json_data['name']) if 'name' in json_data else None,
            action=enums.yasm.internal.person.ContactsPatchActions(json_data['action']) if 'action' in json_data else None,
        )

    @classmethod
    def from_string(cls, data):
        return cls.from_json(json.loads(data))

    def to_json(self):
        self.serialized = True
        ret = dict()

        if isinstance(self.name, str):
            ret['name'] = self.name
        if isinstance(self.action, enums.yasm.internal.person.ContactsPatchActions):
            ret['action'] = self.action.value
        self.serialized = False
        return ret

    def to_string(self):
        return json.dumps(self.to_json())


class CoursesResponse:
    def __init__(
        self,
        courses=None,
    ):
        self.serialized = False
        if courses is not None:
            assert isinstance(courses, list)
            self.courses = courses


    @classmethod
    def from_json(cls, json_data):
        return cls(
            courses=[yasm.yasm.database.Course.from_json(item) for item in json_data.get('courses', [])],
        )

    @classmethod
    def from_string(cls, data):
        return cls.from_json(json.loads(data))

    def to_json(self):
        self.serialized = True
        ret = dict()

        if  isinstance(self.courses, list):
            ret['courses'] = [value.to_json() for value in self.courses if not value.serialized]
        self.serialized = False
        return ret

    def to_string(self):
        return json.dumps(self.to_json())


class FetchPersonRequest:
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


class GetProfileResponse:
    def __init__(
        self,
        id=None,
        first_name=None,
        last_name=None,
        nick_name=None,
        ava=None,
    ):
        self.serialized = False
        if id is not None:
            assert isinstance(id, int)
            self.id = id
        if first_name is not None:
            assert isinstance(first_name, str)
            self.first_name = first_name
        if last_name is not None:
            assert isinstance(last_name, str)
            self.last_name = last_name
        if nick_name is not None:
            assert isinstance(nick_name, str)
            self.nick_name = nick_name
        if ava is not None:
            assert isinstance(ava, str)
            self.ava = ava


    @classmethod
    def from_json(cls, json_data):
        return cls(
            id=int(json_data['id']) if 'id' in json_data else None,
            first_name=str(json_data['first_name']) if 'first_name' in json_data else None,
            last_name=str(json_data['last_name']) if 'last_name' in json_data else None,
            nick_name=str(json_data['nick_name']) if 'nick_name' in json_data else None,
            ava=str(json_data['ava']) if 'ava' in json_data else None,
        )

    @classmethod
    def from_string(cls, data):
        return cls.from_json(json.loads(data))

    def to_json(self):
        self.serialized = True
        ret = dict()

        if isinstance(self.id, int):
            ret['id'] = self.id
        if isinstance(self.first_name, str):
            ret['first_name'] = self.first_name
        if isinstance(self.last_name, str):
            ret['last_name'] = self.last_name
        if isinstance(self.nick_name, str):
            ret['nick_name'] = self.nick_name
        if isinstance(self.ava, str):
            ret['ava'] = self.ava
        self.serialized = False
        return ret

    def to_string(self):
        return json.dumps(self.to_json())


class SetAvaRequest:
    def __init__(
        self,
        new_ava=None,
    ):
        self.serialized = False
        if new_ava is not None:
            assert isinstance(new_ava, str)
            self.new_ava = new_ava


    @classmethod
    def from_json(cls, json_data):
        return cls(
            new_ava=str(json_data['new_ava']) if 'new_ava' in json_data else None,
        )

    @classmethod
    def from_string(cls, data):
        return cls.from_json(json.loads(data))

    def to_json(self):
        self.serialized = True
        ret = dict()

        if isinstance(self.new_ava, str):
            ret['new_ava'] = self.new_ava
        self.serialized = False
        return ret

    def to_string(self):
        return json.dumps(self.to_json())


class SetPasswordRequest:
    def __init__(
        self,
        new_ava=None,
    ):
        self.serialized = False
        if new_ava is not None:
            assert isinstance(new_ava, str)
            self.new_ava = new_ava


    @classmethod
    def from_json(cls, json_data):
        return cls(
            new_ava=str(json_data['new_ava']) if 'new_ava' in json_data else None,
        )

    @classmethod
    def from_string(cls, data):
        return cls.from_json(json.loads(data))

    def to_json(self):
        self.serialized = True
        ret = dict()

        if isinstance(self.new_ava, str):
            ret['new_ava'] = self.new_ava
        self.serialized = False
        return ret

    def to_string(self):
        return json.dumps(self.to_json())


