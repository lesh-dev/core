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
        uselist=False,
        back_populates='person',
    )
    __table_args__ = (
    )



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
        uselist=False,
        back_populates='course',
    )
    __table_args__ = (
    )



class CourseTeacher(db.Model):
    __tablename__ = 'courseteacher'
    fk_person_person_id = db.Column(
        db.Integer,
        name='fk_person_person_id',
        primary_key=True,
        
    )
    fk_course_course_id = db.Column(
        db.Integer,
        name='fk_course_course_id',
        primary_key=True,
        
    )
    person = db.relationship(
        'Person',
        uselist=True,
        foreign_keys=[
            fk_person_person_id,
        ],
        back_populates='courses',
    )
    course = db.relationship(
        'Course',
        uselist=True,
        foreign_keys=[
            fk_course_course_id,
        ],
        back_populates='teachers',
    )
    __table_args__ = (
        db.ForeignKeyConstraint(
            (
                fk_person_person_id,
            ),
            (
                'person.person_id',
            ),
        ),
        db.ForeignKeyConstraint(
            (
                fk_course_course_id,
            ),
            (
                'course.course_id',
            ),
        ),
    )



class B(db.Model):
    __tablename__ = 'b'
    id = db.Column(
        db.Integer,
        name='id',
        primary_key=True,
        autoincrement=True,

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
        uselist=False,
        foreign_keys=[
            fk_a_id,
            fk_a_id2,
        ],
        back_populates='b',
    )
    a2 = db.relationship(
        'A',
        uselist=False,
        back_populates='b2',
    )
    __table_args__ = (
        db.ForeignKeyConstraint(
            (
                fk_a_id,
                fk_a_id2,
            ),
            (
                'a.id',
                'a.id2',
            ),
        ),
    )



class A(db.Model):
    __tablename__ = 'a'
    id = db.Column(
        db.Integer,
        name='id',
        primary_key=True,
        autoincrement=True,

    )
    id2 = db.Column(
        db.Text,
        name='id2',
        primary_key=True,
        
    )
    t = db.Column(
        db.Text,
        name='t',
        nullable=True,

    )
    e_key = db.Column(
        db.Integer,
        name='e_key',
        nullable=True,

    )
    b = db.relationship(
        'B',
        uselist=False,
        back_populates='a',
    )
    c = db.relationship(
        'C',
        uselist=False,
        back_populates='a',
    )
    d = db.relationship(
        'D',
        uselist=False,
        back_populates='a',
    )
    e = db.relationship(
        'E',
        uselist=True,
        foreign_keys=[
            e_key,
        ],
        back_populates='a',
    )
    b2 = db.relationship(
        'B',
        uselist=False,
        back_populates='a2',
    )
    __table_args__ = (
        db.ForeignKeyConstraint(
            (
                e_key,
            ),
            (
                'e.id',
            ),
        ),
    )



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
        uselist=True,
        foreign_keys=[
            fk_a_id,
            fk_a_id2,
        ],
        back_populates='c',
    )
    __table_args__ = (
        db.ForeignKeyConstraint(
            (
                fk_a_id,
                fk_a_id2,
            ),
            (
                'a.id',
                'a.id2',
            ),
        ),
    )



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
        uselist=True,
        foreign_keys=[
            fk_a_id,
            fk_a_id2,
        ],
        back_populates='d',
    )
    __table_args__ = (
        db.ForeignKeyConstraint(
            (
                fk_a_id,
                fk_a_id2,
            ),
            (
                'a.id',
                'a.id2',
            ),
        ),
    )



class E(db.Model):
    __tablename__ = 'e'
    id = db.Column(
        db.Integer,
        name='id',
        primary_key=True,
        
    )
    a = db.relationship(
        'A',
        uselist=False,
        back_populates='e',
    )
    __table_args__ = (
    )


