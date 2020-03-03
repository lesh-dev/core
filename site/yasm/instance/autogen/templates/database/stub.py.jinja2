from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy import or_

db = SQLAlchemy()
lm = LoginManager()


SEARCHABLES = set()


def add_search(cls):
    cls.__bases__ = (*cls.__bases__, SearchableMixin)
    SEARCHABLES.add(cls)
    return cls


def search_all(pattern, tables=None):
    global SEARCHABLES
    for Searchable in SEARCHABLES:
        if tables is None or Searchable.__tablename__ in tables:
            for entry in Searchable.search(pattern):
                yield entry


class SearchableMixin:
    @classmethod
    def search(cls, value):
        return cls.query.filter(or_(*[x.ilike(f'%{value}%') for x in cls.searchable_columns]))