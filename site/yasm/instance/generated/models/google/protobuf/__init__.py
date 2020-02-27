import json
import sqlalchemy
import datetime
from ... import stub
from ... import yasm
from .... import enums



class Empty:
    def __init__(
        self,
    ):
        self.serialized = False


    @classmethod
    def from_json(cls, json_data):
        return cls(
        )

    @classmethod
    def from_string(cls, data):
        return cls.from_json(json.loads(data))

    def to_json(self):
        self.serialized = True
        ret = dict()

        self.serialized = False
        return ret

    def to_string(self):
        return json.dumps(self.to_json())




