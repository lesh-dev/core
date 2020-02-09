from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

db = SQLAlchemy()


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


@add_search
class Person(db.Model):
    __tablename__ = 'person'

    person_id = db.Column(
        db.Integer,
        name='person_id',
        primary_key=True,

    )
    first_name = db.Column(
        db.Text,
        name='first_name',
        
    )
    courses = db.relationship(
        'CourseTeacher',
        back_populates='person',
    )

    __table_args__ = (
    )

    searchable_columns = [
        first_name,
    ]


class Course(db.Model):
    __tablename__ = 'course'

    course_id = db.Column(
        db.Integer,
        name='course_id',
        primary_key=True,

    )
    course_name = db.Column(
        db.Text,
        name='course_name',
        
    )
    s = db.Column(
        db.ARRAY(db.Text),
        name='s',
        
    )
    teachers = db.relationship(
        'CourseTeacher',
        back_populates='course',
    )

    __table_args__ = (
    )

    searchable_columns = [
    ]


class CourseTeacher(db.Model):
    __tablename__ = 'courseteacher'

    fk_person_person_id = db.Column(
        db.Integer,
        name='fk_person_person_id',
        primary_key=True,

    )
    person = db.relationship(
        'Person',
        back_populates='courses',
        foreign_keys=[
            fk_person_person_id,
        ],
    )
    fk_course_course_id = db.Column(
        db.Integer,
        name='fk_course_course_id',
        primary_key=True,

    )
    course = db.relationship(
        'Course',
        back_populates='teachers',
        foreign_keys=[
            fk_course_course_id,
        ],
    )

    __table_args__ = (
    )

    searchable_columns = [
    ]


class A(db.Model):
    __tablename__ = 'a'

    id = db.Column(
        db.Integer,
        name='id',
        primary_key=True,

    )
    id2 = db.Column(
        db.Text,
        name='id2',
        primary_key=True,

    )
    fk_b_id = db.Column(
        db.Integer,
        name='fk_b_id',
        
    )
    fk_b_a = db.Column(
        db.JSON,
        name='fk_b_a',
        
    )
    b = db.relationship(
        'B',
        back_populates='a',
        foreign_keys=[
            fk_b_id,
            fk_b_a,
        ],
    )
    c = db.relationship(
        'C',
        back_populates='a',
    )
    d = db.relationship(
        'D',
        back_populates='a',
    )
    fk_e_id = db.Column(
        db.Integer,
        name='fk_e_id',
        
    )
    e = db.relationship(
        'E',
        back_populates='a',
        foreign_keys=[
            fk_e_id,
        ],
    )
    fk_b2_id = db.Column(
        db.Integer,
        name='fk_b2_id',
        
    )
    fk_b2_a = db.Column(
        db.JSON,
        name='fk_b2_a',
        
    )
    b2 = db.relationship(
        'B',
        back_populates='a2',
        foreign_keys=[
            fk_b2_id,
            fk_b2_a,
        ],
    )

    __table_args__ = (
    )

    searchable_columns = [
    ]


class B(db.Model):
    __tablename__ = 'b'

    id = db.Column(
        db.Integer,
        name='id',
        primary_key=True,

    )
    fk_a_id = db.Column(
        db.Integer,
        name='fk_a_id',
        primary_key=True,

    )
    fk_a_id2 = db.Column(
        db.Text,
        name='fk_a_id2',
        primary_key=True,

    )
    a = db.relationship(
        'A',
        back_populates='b',
        foreign_keys=[
            fk_a_id,
            fk_a_id2,
        ],
    )
    fk_a2_id = db.Column(
        db.Integer,
        name='fk_a2_id',
        
    )
    fk_a2_id2 = db.Column(
        db.Text,
        name='fk_a2_id2',
        
    )
    a2 = db.relationship(
        'A',
        back_populates='b2',
        foreign_keys=[
            fk_a2_id,
            fk_a2_id2,
        ],
    )

    __table_args__ = (
    )

    searchable_columns = [
    ]


class C(db.Model):
    __tablename__ = 'c'

    id = db.Column(
        db.Integer,
        name='id',
        primary_key=True,

    )
    fk_a_id = db.Column(
        db.Integer,
        name='fk_a_id',
        
    )
    fk_a_id2 = db.Column(
        db.Text,
        name='fk_a_id2',
        
    )
    a = db.relationship(
        'A',
        back_populates='c',
        foreign_keys=[
            fk_a_id,
            fk_a_id2,
        ],
    )

    __table_args__ = (
    )

    searchable_columns = [
    ]


class D(db.Model):
    __tablename__ = 'd'

    id = db.Column(
        db.Integer,
        name='id',
        primary_key=True,

    )
    fk_a_id = db.Column(
        db.Integer,
        name='fk_a_id',
        
    )
    fk_a_id2 = db.Column(
        db.Text,
        name='fk_a_id2',
        
    )
    a = db.relationship(
        'A',
        back_populates='d',
        foreign_keys=[
            fk_a_id,
            fk_a_id2,
        ],
    )

    __table_args__ = (
    )

    searchable_columns = [
    ]


class E(db.Model):
    __tablename__ = 'e'

    id = db.Column(
        db.Integer,
        name='id',
        primary_key=True,

    )
    a = db.relationship(
        'A',
        back_populates='e',
    )

    __table_args__ = (
    )

    searchable_columns = [
    ]

