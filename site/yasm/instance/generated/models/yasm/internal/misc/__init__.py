import json
import sqlalchemy
import datetime
from flask_login import UserMixin

from .... import stub
from .... import yasm
from ..... import enums


class SearchRequest:
    def __init__(
        self,
        query=None,
    ):
        self.serialized = False
        if query is not None:
            assert isinstance(query, str)
            self.query = query


    @classmethod
    def from_json(cls, json_data):
        return cls(
            query=str(json_data['query']) if 'query' in json_data else None,
        )

    @classmethod
    def from_string(cls, data):
        return cls.from_json(json.loads(data))

    def to_json(self):
        self.serialized = True
        ret = dict()

        if isinstance(self.query, str):
            ret['query'] = self.query
        self.serialized = False
        return ret

    def to_string(self):
        return json.dumps(self.to_json())


class SearchResult:
    def __init__(
        self,
        search_url=None,
        data=None,
    ):
        self.serialized = False
        if search_url is not None:
            assert isinstance(search_url, str)
            self.search_url = search_url
        if data is not None:
            assert isinstance(data, dict)
            self.data = data


    @classmethod
    def from_json(cls, json_data):
        return cls(
            search_url=str(json_data['search_url']) if 'search_url' in json_data else None,
            data={str(key): str(value) for key, value in json_data['data']} if 'data' in json_data else None,
        )

    @classmethod
    def from_string(cls, data):
        return cls.from_json(json.loads(data))

    def to_json(self):
        self.serialized = True
        ret = dict()

        if isinstance(self.search_url, str):
            ret['search_url'] = self.search_url
        if  isinstance(self.data, dict):
            ret['data'] = {key: self.value for key, value in self.data}
        self.serialized = False
        return ret

    def to_string(self):
        return json.dumps(self.to_json())


class SearchResponse:
    def __init__(
        self,
        query=None,
        results=None,
    ):
        self.serialized = False
        if query is not None:
            assert isinstance(query, str)
            self.query = query
        if results is not None:
            assert isinstance(results, list)
            self.results = results


    @classmethod
    def from_json(cls, json_data):
        return cls(
            query=str(json_data['query']) if 'query' in json_data else None,
            results=[yasm.yasm.internal.misc.SearchResult.from_json(item) for item in json_data.get('results', [])],
        )

    @classmethod
    def from_string(cls, data):
        return cls.from_json(json.loads(data))

    def to_json(self):
        self.serialized = True
        ret = dict()

        if isinstance(self.query, str):
            ret['query'] = self.query
        if  isinstance(self.results, list):
            ret['results'] = [value.to_json() for value in self.results if not value.serialized]
        self.serialized = False
        return ret

    def to_string(self):
        return json.dumps(self.to_json())


