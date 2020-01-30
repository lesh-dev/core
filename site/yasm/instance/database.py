"""
.. _database:

ORM declaration file
"""
from types import MethodType
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.inspection import inspect
from sqlalchemy import or_

db = SQLAlchemy()


class EntryStates(db.Enum): # should we move this to generator?
    RELEVANT = 'RELEVANT'
    OUTDATED = 'OUTDATED'


SEARCHABLES = set()


def search_all(pattern, tables=None):
    global SEARCHABLES
    for Searchable in SEARCHABLES:
        if tables is None or Searchable.__tablename__ in tables:
            for entry in Searchable.search(pattern):
                yield entry.as_search_result()


class SearchableMixin:
    @classmethod
    def search(cls, value):
        return cls.query.filter(or_(*[x.ilike(f'%{value}%') for x in inspect(cls).columns.values() if x.searchable]))

    def as_search_result(self):
        id_name = self.__tablename__ + '_id'
        return {
            'search_url': f'/i/{self.__tablename__}/{getattr(self, id_name)}',
            'data': {
                field.name: getattr(self, field.name)
                for field in inspect(self.__class__).columns.values()
                if field.searchable or field.name == id_name
            },
        }


def add_search(cls):
    cls.__bases__ = (*cls.__bases__, SearchableMixin)
    SEARCHABLES.add(cls)
    return cls


class SerializerMixin(object):

    def serialize(self):
        return {
            c: getattr(self, c).serialize() if
            hasattr(getattr(self, c), 'serialize') else
            getattr(self, c)
            for c in inspect(self).attrs.keys()
            if c != '_sa_instance_state' and not hasattr(getattr(self, c), 'all')
        }

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]


class MarkedForeignKey(db.ForeignKey):

    def __init__(self, col, *args, **kwargs):
        if isinstance(col, str):
            self.referenced_model = col.split('.')[0]
        else:
            self.referenced_model = col.parent
        super().__init__(col, *args, **kwargs)

    def model(self):
        return self.referenced_model


class MetaColumn(db.Column):
    """
    Wrapper around SQLAlchemy.Column, which allows
    giving nicknames to columns,
    """
    nick = ""
    searchable = False

    def __init__(self, *args, nick="", searchable=False, **kwargs):
        """
        :param args: args for Column.__init__
        :param nick: nickname for column
        :param kwargs: kwargs for Column.__init__
        """
        self.nick = nick
        self.searchable = searchable
        super().__init__(*args, **kwargs)
        if self.nick is None:
            self.nick = self.name


# notification
class Notification(db.Model, SerializerMixin):
    __tablename__ = 'notification'
    notification_id = MetaColumn(db.Integer,
                                 nick="id",
                                 primary_key=True,
                                 autoincrement=True)
    mail_group = MetaColumn(db.Text,
                            nick="группа",
                            nullable=False)
    notification_text = MetaColumn(db.Text,
                                   nick="текст",
                                   nullable=False)
    notification_html = MetaColumn(db.Text,
                                   nick="html",
                                   nullable=False)


@add_search
class Department(db.Model, SerializerMixin):
    __tablename__ = 'department'
    department_id = MetaColumn(db.Integer,
                               nick="id",
                               primary_key=True,
                               autoincrement=True)
    department_title = MetaColumn(db.Text,
                                  nick="название",
                                  searchable=True,
                                  nullable=False)
    department_created = MetaColumn(db.Text,
                                    nick="дата создания",
                                    nullable=False)
    department_modified = MetaColumn(db.Text,
                                     nick="последняя модификация",
                                     nullable=False)
    department_changedby = MetaColumn(db.Text,
                                      nick="изменивший",
                                      nullable=False)
    person_schools = db.relationship('PersonSchool', back_populates='department', lazy='dynamic')
    persons = db.relationship('Person', back_populates='department', lazy='dynamic')


@add_search
class Person(UserMixin, db.Model, SerializerMixin):
    __tablename__ = 'person'

    person_id = MetaColumn(db.Integer,
                           nick="id",
                           primary_key=True,
                           autoincrement=True)

    def get_id(self):
        return self.person_id

    rights = MetaColumn(db.Text,
                        nick='права',
                        nullable=True)
    last_name = MetaColumn(db.Text,
                           nick="фамилия",
                           searchable=True,
                           nullable=False)  # фамилия
    first_name = MetaColumn(db.Text,
                            nick="имя",
                            searchable=True,
                            nullable=False)  # имя
    patronymic = MetaColumn(db.Text,
                            nick="отчество",
                            searchable=True,
                            nullable=True)  # отчество
    nick_name = MetaColumn(db.Text,
                           nick="прозвище",
                           searchable=True,
                           nullable=True)  # кличка #569

    birth_date = MetaColumn(db.Text,
                            nick="дата рождения",
                            nullable=False)  # дата рождения
    passport_data = MetaColumn(db.Text,
                               nick="паспортные данные",
                               nullable=False)  # паспортные данные

    school = MetaColumn(db.Text,
                        nick="школа",
                        nullable=False)  # школа, в которой учится школьник
    school_city = MetaColumn(db.Text,
                             nick="город",
                             nullable=False)  # город, в котором находится школа
    ank_class = MetaColumn(db.Text,
                           nick="класс подачи заявки",
                           nullable=False)  # класс подачи заявки
    current_class = MetaColumn(db.Text,
                               nick="текущий класс",
                               nullable=False)  # текущий класс

    phone = MetaColumn(db.Text,
                       nick="городской",
                       searchable=True,
                       nullable=True)  # телефон (городской)
    cellular = MetaColumn(db.Text,
                          nick="мобильный",
                          searchable=True,
                          nullable=True)  # мобильный телефон
    email = MetaColumn(db.Text,
                       searchable=True,
                       nullable=True)  # контактный email
    skype = MetaColumn(db.Text,
                       nullable=True)  # skype
    social_profile = MetaColumn(db.Text,
                                nick="профиль в соц. сети",
                                nullable=True)  # профиль ВКонтакте и т.п. (используемый!)

    is_teacher = MetaColumn(db.Text,
                            nick="препод",
                            nullable=True)  # типично препод
    is_student = MetaColumn(db.Text,
                            nick="школьник",
                            nullable=True)  # типично школьник

    favourites = MetaColumn(db.Text,
                            nick="любимые предметы",
                            nullable=True)  # любимые предметы
    achievements = MetaColumn(db.Text,
                              nick="достижения",
                              nullable=True)  # достижения
    hobby = MetaColumn(db.Text,
                       nick="хобби",
                       nullable=True)  # хобби

    lesh_ref = MetaColumn(db.Text,
                          nick="откуда узнал",
                          nullable=True)  # откуда узнали о школе (2.1+)

    forest_1 = MetaColumn(db.Text,
                          nick="1-й выход в лес",
                          nullable=True)  # 1-й выход в лес (2.3a+)
    forest_2 = MetaColumn(db.Text,
                          nick="2-й выход в лес",
                          nullable=True)  # 2-й выход в лес (2.3a+)
    forest_3 = MetaColumn(db.Text,
                          nick="3-й выход в лес",
                          nullable=True)  # 3-й выход в лес (2.3a+)

    tent_capacity = MetaColumn(db.Text,
                               nick="мест в палатке",
                               nullable=True)  # количество мест в палатке (0 = палатки нет) (2.2+)
    tour_requisites = MetaColumn(db.Text,
                                 nick="тур. инвентарь",
                                 nullable=True)  # имеющиеся предметы туристского обихода (2.2+)

    anketa_status = MetaColumn(
        db.Enum(
            'progress',
            'nextyear',
            'duplicate',
            'reserved',
            'cont',
            'old',
            'new',
            'processed',
            'declined',
            'taken',
            'duplicated',
            'spam',
            'discuss',
            'less',
            'verify',
            name='ank_status'
        ),
        nick="статус анкеты",
        nullable=False,
    )

    user_agent = MetaColumn(db.Text,
                            nick="браузер",
                            nullable=True)  # идентификатор браузера, с которого была подана анкета

    department_id = MetaColumn(db.Integer,
                               MarkedForeignKey(Department.department_id),
                               nick="отделение",
                               nullable=False)  # ссылка на отделение(2.7 +)
    department = db.relationship('Department', lazy='joined')
    person_created = MetaColumn(db.Text,
                                nick="дата создания",
                                nullable=True)  # utc timestamp
    person_modified = MetaColumn(db.Text,
                                 nick="последняя модификация",
                                 nullable=True)  # utc timestamp
    person_changedby = MetaColumn(db.Text,
                                  nick="дата создания",
                                  nullable=True)  # user name

    other_contacts = MetaColumn(
        db.Text,
        nick='WIP/TMP дополнительные контакты (родители)',
        nullable=True,
    )

    person_comments = db.relationship('PersonComment', back_populates='blamed_person', lazy='dynamic')
    person_schools = db.relationship('PersonSchool', back_populates='member_person', lazy='dynamic')
    exams = db.relationship('Exam', back_populates='student', lazy='dynamic')
    course_teachers = db.relationship('CourseTeachers', back_populates='course_teacher', lazy='dynamic')
    contacts = db.relationship('Contact', back_populates='person', lazy='dynamic')
    direct_login = db.relationship('DirectLogin', back_populates='person', lazy='dynamic')
    avas = db.relationship('Ava', back_populates='person', lazy='dynamic')
    # quests = db.relationship('Quest', back_populates='person', lazy='dynamic')


class Ava(db.Model, SerializerMixin):
    __tablename__ = 'ava'
    id = MetaColumn(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        nick='Id'
    )
    person_id = MetaColumn(
        db.Integer,
        MarkedForeignKey(Person.person_id),
        nick='человек',
        nullable=False,
        index=True,
    )
    ava = MetaColumn(
        db.Text,
        nick='картинка',
        nullable=False,
    )
    entry_state = MetaColumn(
        db.Text,
        nick='статус',
        nullable=False,
        index=True,
        default=EntryStates.RELEVANT
    )

    person = db.relationship('Person', lazy='noload', back_populates='avas')


class DirectLogin(db.Model, SerializerMixin):
    __tablename__ = 'direct_login'
    type = MetaColumn(db.String,
                      nick='тип авторизации',
                      primary_key=True)
    person_id = MetaColumn(db.Integer,
                           MarkedForeignKey(Person.person_id),
                           nick='человек',
                           primary_key=True)
    login = MetaColumn(db.Text,
                       nick='логин',
                       nullable=False)
    password_hash = MetaColumn(db.Text,
                               nick='хэш пароля',
                               nullable=False)
    person = db.relationship('Person', lazy='joined')


class Contact(db.Model, SerializerMixin):
    __tablename__ = 'contact'
    id = MetaColumn(db.Integer,
                    nick='id',
                    primary_key=True,
                    autoincrement=True)
    person_id = MetaColumn(
        db.Integer,
        MarkedForeignKey(Person.person_id),
        nick='человек',
        nullable=False
    )
    person = db.relationship(
        'Person',
        lazy='joined'
    )
    name = MetaColumn(
        db.Text,
        nick='название',
        nullable=False
    )
    value = MetaColumn(
        db.Text,
        nick='значение',
        nullable=False
    )


@add_search
class School(db.Model, SerializerMixin):
    __tablename__ = 'school'
    school_id = MetaColumn(db.Integer,
                           nick="id",
                           primary_key=True,
                           autoincrement=True)
    school_title = MetaColumn(db.Text,
                              nick="название",
                              searchable=True,
                              nullable=False)
    school_type = MetaColumn(
        db.Enum(
            'lesh',
            'vesh',
            'zesh',
            'summer',
            'summmer',
            'winter',
            'spring',
            name='school_type'),
        nick="тип",
        nullable=False)  # enum:(летняя, зимняя, весенняя) TODO: simplify
    school_date_start = MetaColumn(
        db.Text,
        nick="дата начала",
        searchable=True,
        nullable=False
    )  # дата начала
    school_date_end = MetaColumn(
        db.Text,
        nick="дата конца",
        searchable=True,
        nullable=False
    )  # дата конца
    school_location = MetaColumn(
        db.Text,
        nick="место проведения",
        searchable=True,
        nullable=False
    )  # место проведения (2.7+)
    school_coords = MetaColumn(
        db.Text,
        nick="координаты проведения",
        searchable=True,
        nullable=False
    )  # координаты
    school_created = MetaColumn(
        db.Text,
        nick="дата создания",
        nullable=False
    )  # utc timestamp
    school_modified = MetaColumn(
        db.Text,
        nick="последнее изменение",
        nullable=False
    )  # utc timestamp
    school_changedby = MetaColumn(db.Text,
                                  nick="изменивший",
                                  nullable=False)  # user name
    person_comments = db.relationship('PersonComment', back_populates='school', lazy='dynamic')
    person_schools = db.relationship('PersonSchool', back_populates='school', lazy='dynamic')
    courses = db.relationship('Course', back_populates='school', lazy='dynamic')


@add_search
class Course(db.Model, SerializerMixin):
    __tablename__ = 'course'
    course_id = MetaColumn(db.Integer,
                           nick="id",
                           primary_key=True,
                           autoincrement=True)
    course_title = MetaColumn(db.Text,
                              nick="название",
                              searchable=True,
                              nullable=False)  # название курса
    school_id = MetaColumn(db.Integer,
                           MarkedForeignKey(School.school_id),
                           nick="школа",
                           nullable=False)  # ссылка на школу, на которой читали курс
    school = db.relationship('School', lazy='joined')
    course_cycle = MetaColumn(db.Text,
                              nick="цикл",
                              nullable=True)  # цикл, на котором читался курс
    target_class = MetaColumn(db.Text,
                              nick="целевая аудитория",
                              nullable=True)  # диапазон классов, на которые рассчитан курс
    course_desc = MetaColumn(db.Text,
                             nick="описание",
                             searchable=True,
                             nullable=True)  # описание курса
    course_type = MetaColumn(
        db.Enum(
            'generic',
            'other',
            'facult',
            'prac',
            'single',
            name="course_type"
        ),
        nick="тип",
        nullable=False)  # тип курса(прак, поход, etc)
    course_area = MetaColumn(
        db.Enum(
            'cs',
            'unknown',
            'nature',
            'precise',
            'other',
            'human',
            name="course_area"),
        nick="область",
        nullable=False)  # предметная область
    course_comment = MetaColumn(db.Text,
                                nick="комментарий",
                                nullable=True)  # комментарий к курсу(чатик пока не делаем)
    course_created = MetaColumn(db.Text,
                                nick="дата создания",
                                nullable=False)  # utc timestamp
    course_modified = MetaColumn(db.Text,
                                 nick="последнее изменение",
                                 nullable=False)  # utc timestamp
    course_changedby = MetaColumn(db.Text,
                                  nick="изменивший",
                                  nullable=False)  # user name
    exams = db.relationship('Exam', back_populates='course', lazy='dynamic')
    course_teachers = db.relationship('CourseTeachers', back_populates='course', lazy='dynamic')


class CourseTeachers(db.Model, SerializerMixin):
    __tablename__ = 'course_teachers'
    course_teachers_id = MetaColumn(db.Integer,
                                    nick="id",
                                    primary_key=True,
                                    autoincrement=True)
    course_id = MetaColumn(db.Integer,
                           MarkedForeignKey(Course.course_id),
                           nick="курс",
                           nullable=False)
    course = db.relationship('Course', lazy='joined')
    course_teacher_id = MetaColumn(db.Integer,
                                   MarkedForeignKey(Person.person_id),
                                   nick="перпод",
                                   nullable=False)
    course_teacher = db.relationship('Person', lazy='joined')
    course_teachers_created = MetaColumn(db.Text,
                                         nick="дата создания",
                                         nullable=False)  # utc timestampcourse_teacher
    course_teachers_modified = MetaColumn(db.Text,
                                          nick="последнее изменение",
                                          nullable=False)  # utc timestamp
    course_teachers_changedby = MetaColumn(db.Text,
                                           nick="изменивший",
                                           nullable=False)  # user name


class Exam(db.Model, SerializerMixin):
    __tablename__ = 'exam'
    exam_id = MetaColumn(db.Integer,
                         nick="id",
                         primary_key=True,
                         autoincrement=True)  # not used
    student_person_id = MetaColumn(db.Integer,
                                   MarkedForeignKey(Person.person_id),
                                   nick="школьник",
                                   nullable=False)
    student = db.relationship('Person', lazy='joined')
    course_id = MetaColumn(db.Integer,
                           MarkedForeignKey(Course.course_id),
                           nick="курс",
                           nullable=False)
    course = db.relationship('Course', lazy='joined')
    exam_status = MetaColumn(db.Text,
                             nick="статус",
                             nullable=True)
    deadline_date = MetaColumn(db.Text,
                               nick="дедлайн",
                               nullable=True)
    exam_comment = MetaColumn(db.Text,
                              nick="комментарий",
                              nullable=True)
    exam_created = MetaColumn(db.Text,
                              nick="дата создания",
                              nullable=False)  # utc timestamp
    exam_modified = MetaColumn(db.Text,
                               nick="последнее изменение",
                               nullable=False)  # utc timestamp
    exam_changedby = MetaColumn(db.Text,
                                nick="изменивший",
                                nullable=False)  # user name


class PersonSchool(db.Model, SerializerMixin):
    __tablename__ = 'person_school'
    person_school_id = MetaColumn(db.Integer,
                                  nick="id",
                                  primary_key=True,
                                  autoincrement=True)
    member_person_id = MetaColumn(db.Integer,
                                  MarkedForeignKey(Person.person_id),
                                  nick="участник",
                                  nullable=False)  # fk person
    member_person = db.relationship('Person', lazy='joined')
    member_department_id = MetaColumn(db.Integer,
                                      MarkedForeignKey(Department.department_id),
                                      nick="отделение",
                                      nullable=False)  # fk department
    department = db.relationship('Department', lazy='joined')
    school_id = MetaColumn(db.Integer,
                           MarkedForeignKey(School.school_id),
                           nick="школа",
                           nullable=False)  # fk school
    school = db.relationship('School', lazy='joined')
    is_student = MetaColumn(db.Text,
                            nick="школьник",
                            nullable=True)  # является ли школьником на данной школе
    is_teacher = MetaColumn(db.Text,
                            nick="препод",
                            nullable=True)  # является ли преподом на данной школе
    curatorship = MetaColumn(
        db.Enum(
            '',
            'none',
            'assist',
            'cur',
            name='curatorship_type'),
        nick="кураторство",
        nullable=True)  # кураторство на данной школе enum: (никто, помкур, куратор)
    curator_group = MetaColumn(db.Text,
                               nick="группа кураторства",
                               nullable=True)  # группа кураторства
    # класс, в котором находится школьник
    # (для Летней школы надо договориться, какой именно класс мы ставим, -- будущий или прошедший)
    current_class = MetaColumn(db.Text,
                               nick="класс",
                               nullable=True)
    courses_needed = MetaColumn(db.Text,
                                nick="необходимое количество курсов",
                                nullable=True)  # потребное кол - во курсов для сдачи на школе
    person_school_comment = MetaColumn(db.Text,
                                       nick="комментарий",
                                       nullable=True)  # комментарий(v2.10)
    person_school_created = MetaColumn(db.Text,
                                       nick="дата создания",
                                       nullable=False)  # utc timestamp
    person_school_modified = MetaColumn(db.Text,
                                        nick="последнее изменение",
                                        nullable=False)  # utc timestamp
    person_school_changedby = MetaColumn(db.Text,
                                         nick="изменивший",
                                         nullable=False)  # user name
    frm = MetaColumn(db.Text,
                     nick="заезд", )
    tll = MetaColumn(db.Text,
                     nick="отъезд", )

    calendars = db.relationship('Calendar', back_populates='person_school')


class Calendar(db.Model, SerializerMixin):
    __tablename__ = 'calendar'

    person_school_id = MetaColumn(
        db.Integer,
        MarkedForeignKey(PersonSchool.person_school_id),
        nick="person_school",
        nullable=False,
        primary_key=True
    )
    person_school = db.relationship(PersonSchool)
    date = MetaColumn(
        db.DATE,
        nick="дата",
        nullable=False,
        primary_key=True
    )
    status = MetaColumn(
        db.Text,
        nick='статус',
        nullable=False)
    calendar_modified = MetaColumn(
        db.TIMESTAMP,
        nick='время',
        nullable=False,
    )
    changed_by = MetaColumn(
        db.Text,
        nick='изменивший',
        nullable=False
    )


class PersonComment(db.Model, SerializerMixin):
    __tablename__ = 'person_comment'
    person_comment_id = MetaColumn(db.Integer,
                                   nick="id",
                                   primary_key=True,
                                   autoincrement=True)
    comment_text = MetaColumn(db.Text,
                              nick="комментарий",
                              nullable=True)  # текст комментария
    blamed_person_id = MetaColumn(db.Integer,
                                  MarkedForeignKey(Person.person_id),
                                  nick="упомянутый",
                                  nullable=False)  # fk person - - сабжевый участник(типично школьник)
    blamed_person = db.relationship('Person', lazy='joined')
    school_id = MetaColumn(db.Integer,
                           MarkedForeignKey(School.school_id),
                           nick="школа",
                           nullable=False)  # fk school - - школа, о которой идёт речь(v2.15)
    school = db.relationship('School', lazy='joined')
    owner_login = MetaColumn(db.Text,
                             nick="автор",
                             nullable=False)  # логин автора комментария
    record_acl = MetaColumn(db.Text,
                            nullable=True)  # ACL(v2.15)
    person_comment_created = MetaColumn(db.Text,
                                        nick="дата создания",
                                        nullable=False)  # utc timestamp
    person_comment_modified = MetaColumn(db.Text,
                                         nick="последние изменение",
                                         nullable=False)  # utc timestamp
    person_comment_deleted = MetaColumn(db.Text,
                                        nick="дата удаления",
                                        nullable=True)  # признак удаления(из базы ничего удалить нельзя)
    person_comment_changedby = MetaColumn(db.Text,
                                          nick="изменивший",
                                          nullable=False)  # user name


# class Quest(db.Model, Serializer):
#     __tablename__ = 'quest'
#     id = NamedColumn(
#         db.Integer,
#         nick='id',
#         primary_key=True,
#         autoincrement=True
#     )
#     name = NamedColumn(
#         db.String,
#         nick='название',
#         nullable=False,
#     )
#     text = NamedColumn(
#         db.Text,
#         nick='текст',
#         nullable=False,
#     )
#     creator = NamedColumn(
#         db.Integer,
#         MarkedForeignKey(Person.person_id),
#         nick='создатель',
#         nullable=False,
#     )
#     admins = NamedColumn(
#         db.JSON,
#         nick='проверяющие',
#         nullable=False,
#     )
#     assignee = NamedColumn(
#         db.JSON,
#         nick='сдающие',
#         nullable=False,
#     )
#     progress = NamedColumn(
#         db.Integer,
#         nick='прогресс %',
#         nullable=False,
#     )
#     blocks = NamedColumn(
#         db.Integer,
#         MarkedForeignKey('quest.id'),
#         nick='блокирует',
#         nullable=True
#     )
#     blockers = db.relationship('Quest', back_populates='blocks', lazy='dynamic')
#     person = db.relationship('Person', lazy='joined')


# contest TODO: nickname columns
class Submission(db.Model, SerializerMixin):
    __tablename__ = 'submission'
    submission_id = MetaColumn(db.Integer,
                               primary_key=True,
                               autoincrement=True)
    mail = MetaColumn(db.Text,
                      nullable=True)
    attachment = MetaColumn(db.Text,
                            nullable=True)
    fileexchange = MetaColumn(db.Text,
                              nullable=True)
    submission_timestamp = MetaColumn(db.Text,
                                      nullable=True)
    sender = MetaColumn(db.Text,
                        nullable=True)
    replied = MetaColumn(db.Text,
                         nullable=True)
    processed = MetaColumn(db.Text,
                           nullable=True)
    contest_year = MetaColumn(db.Text,
                              nullable=True)


class Contestants(db.Model, SerializerMixin):
    __tablename__ = 'contestants'
    contestants_id = MetaColumn(db.Integer,
                                primary_key=True,
                                autoincrement=True)
    name = MetaColumn(db.Text,
                      nullable=True)
    mail = MetaColumn(db.Text,
                      nullable=True)
    phone = MetaColumn(db.Text,
                       nullable=True)
    parents = MetaColumn(db.Text,
                         nullable=True)
    address = MetaColumn(db.Text,
                         nullable=True)
    school = MetaColumn(db.Text,
                        nullable=True)
    level = MetaColumn(db.Text,
                       nullable=True)
    teacher_name = MetaColumn(db.Text,
                              nullable=True)
    work = MetaColumn(db.Text,
                      nullable=True)
    fileexchange = MetaColumn(db.Text,
                              nullable=True)
    status = MetaColumn(db.Text,
                        nullable=True)
    contest_year = MetaColumn(db.Text,
                              nullable=True)
    solutions = db.relationship('Solutions', back_populates='contestant', lazy='dynamic')


class Problems(db.Model, SerializerMixin):
    __tablename__ = 'problems'
    problems_id = MetaColumn(db.Integer,
                             primary_key=True,
                             autoincrement=True)
    contest_year = MetaColumn(db.Text,
                              nullable=True)
    problem_name = MetaColumn(db.Text,
                              nullable=True)
    problem_html = MetaColumn(db.Text,
                              nullable=True)
    people = MetaColumn(db.Text,
                        nullable=True)
    criteria = MetaColumn(db.Text,
                          nullable=True)
    solutions = db.relationship('Solutions', back_populates='problem', lazy='dynamic')


class Solutions(db.Model, SerializerMixin):
    __tablename__ = 'solutions'
    solutions_id = MetaColumn(db.Integer,
                              primary_key=True,
                              autoincrement=True)
    problem_id = MetaColumn(db.Integer,
                            MarkedForeignKey(Problems.problems_id),
                            nullable=False)
    problem = db.relationship('Problems', lazy='joined')
    contest_year = MetaColumn(db.Text,
                              nullable=True)
    contestant_id = MetaColumn(db.Integer,
                               MarkedForeignKey(Contestants.contestants_id),
                               nullable=False)
    contestant = db.relationship('Contestants', lazy='joined')
    resolution_text = MetaColumn(db.Text,
                                 nullable=True)
    resolution_author = MetaColumn(db.Text,
                                   nullable=True)
    resolution_mark = MetaColumn(db.Text,
                                 nullable=True)


registered_models = [  # needed for sql checks
    Notification,
    Department,
    Person,
    Course,
    CourseTeachers,
    Exam,
    School,
    PersonSchool,
    PersonComment,
    Submission,
    Contestants,
    Problems,
    Solutions
]


def db_read_test():
    """
    Checks if all items stored in database are readable by this ORM
    :return: None
    """
    for i in registered_models:
        print(i.query.all())
