"""
.. _database:

ORM declaration file
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.inspection import inspect

db = SQLAlchemy()


class EntryStates(db.Enum): # should we move this to generator?
    RELEVANT = 'RELEVANT'
    OUTDATED = 'OUTDATED'


class Serializer(object):

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


class NamedColumn(db.Column):
    """
    Wrapper around SQLAlchemy.Column, which allows
    giving nicknames to columns,
    """
    nick = ""

    def __init__(self, *args, nick="", **kwargs):
        """
        :param args: args for Column.__init__
        :param nick: nickname for column
        :param kwargs: kwargs for Column.__init__
        """
        self.nick = nick
        super().__init__(*args, **kwargs)
        if self.nick is None:
            self.nick = self.name


# notification
class Notification(db.Model, Serializer):
    __tablename__ = 'notification'
    notification_id = NamedColumn(db.Integer,
                                  nick="id",
                                  primary_key=True,
                                  autoincrement=True)
    mail_group = NamedColumn(db.Text,
                             nick="группа",
                             nullable=False)
    notification_text = NamedColumn(db.Text,
                                    nick="текст",
                                    nullable=False)
    notification_html = NamedColumn(db.Text,
                                    nick="html",
                                    nullable=False)


# XSM
class Department(db.Model, Serializer):
    __tablename__ = 'department'
    department_id = NamedColumn(db.Integer,
                                nick="id",
                                primary_key=True,
                                autoincrement=True)
    department_title = NamedColumn(db.Text,
                                   nick="название",
                                   nullable=False)
    department_created = NamedColumn(db.Text,
                                     nick="дата создания",
                                     nullable=False)
    department_modified = NamedColumn(db.Text,
                                      nick="последняя модификация",
                                      nullable=False)
    department_changedby = NamedColumn(db.Text,
                                       nick="изменивший",
                                       nullable=False)
    person_schools = db.relationship('PersonSchool', back_populates='department', lazy='dynamic')
    persons = db.relationship('Person', back_populates='department', lazy='dynamic')


class Person(UserMixin, db.Model, Serializer):
    __tablename__ = 'person'
    person_id = NamedColumn(db.Integer,
                            nick="id",
                            primary_key=True,
                            autoincrement=True)

    def get_id(self):
        return self.person_id

    rights = NamedColumn(db.Text,
                         nick='права',
                         nullable=True)
    last_name = NamedColumn(db.Text,
                            nick="фамилия",
                            nullable=False)  # фамилия
    first_name = NamedColumn(db.Text,
                             nick="имя",
                             nullable=False)  # имя
    patronymic = NamedColumn(db.Text,
                             nick="отчество",
                             nullable=True)  # отчество
    nick_name = NamedColumn(db.Text,
                            nick="прозвище",
                            nullable=True)  # кличка #569

    birth_date = NamedColumn(db.Text,
                             nick="дата рождения",
                             nullable=False)  # дата рождения
    passport_data = NamedColumn(db.Text,
                                nick="паспортные данные",
                                nullable=False)  # паспортные данные

    school = NamedColumn(db.Text,
                         nick="школа",
                         nullable=False)  # школа, в которой учится школьник
    school_city = NamedColumn(db.Text,
                              nick="город",
                              nullable=False)  # город, в котором находится школа
    ank_class = NamedColumn(db.Text,
                            nick="класс подачи заявки",
                            nullable=False)  # класс подачи заявки
    current_class = NamedColumn(db.Text,
                                nick="текущий класс",
                                nullable=False)  # текущий класс

    phone = NamedColumn(db.Text,
                        nick="городской",
                        nullable=True)  # телефон (городской)
    cellular = NamedColumn(db.Text,
                           nick="мобильный",
                           nullable=True)  # мобильный телефон
    email = NamedColumn(db.Text,
                        nullable=True)  # контактный email
    skype = NamedColumn(db.Text,
                        nullable=True)  # skype
    social_profile = NamedColumn(db.Text,
                                 nick="профиль в соц. сети",
                                 nullable=True)  # профиль ВКонтакте и т.п. (используемый!)

    is_teacher = NamedColumn(db.Text,
                             nick="препод",
                             nullable=True)  # типично препод
    is_student = NamedColumn(db.Text,
                             nick="школьник",
                             nullable=True)  # типично школьник

    favourites = NamedColumn(db.Text,
                             nick="любимые предметы",
                             nullable=True)  # любимые предметы
    achievements = NamedColumn(db.Text,
                               nick="достижения",
                               nullable=True)  # достижения
    hobby = NamedColumn(db.Text,
                        nick="хобби",
                        nullable=True)  # хобби

    lesh_ref = NamedColumn(db.Text,
                           nick="откуда узнал",
                           nullable=True)  # откуда узнали о школе (2.1+)

    forest_1 = NamedColumn(db.Text,
                           nick="1-й выход в лес",
                           nullable=True)  # 1-й выход в лес (2.3a+)
    forest_2 = NamedColumn(db.Text,
                           nick="2-й выход в лес",
                           nullable=True)  # 2-й выход в лес (2.3a+)
    forest_3 = NamedColumn(db.Text,
                           nick="3-й выход в лес",
                           nullable=True)  # 3-й выход в лес (2.3a+)

    tent_capacity = NamedColumn(db.Text,
                                nick="мест в палатке",
                                nullable=True)  # количество мест в палатке (0 = палатки нет) (2.2+)
    tour_requisites = NamedColumn(db.Text,
                                  nick="тур. инвентарь",
                                  nullable=True)  # имеющиеся предметы туристского обихода (2.2+)

    anketa_status = NamedColumn(
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

    user_agent = NamedColumn(db.Text,
                             nick="браузер",
                             nullable=True)  # идентификатор браузера, с которого была подана анкета

    department_id = NamedColumn(db.Integer,
                                MarkedForeignKey(Department.department_id),
                                nick="отделение",
                                nullable=False)  # ссылка на отделение(2.7 +)
    department = db.relationship('Department', lazy='joined')
    person_created = NamedColumn(db.Text,
                                 nick="дата создания",
                                 nullable=True)  # utc timestamp
    person_modified = NamedColumn(db.Text,
                                  nick="последняя модификация",
                                  nullable=True)  # utc timestamp
    person_changedby = NamedColumn(db.Text,
                                   nick="дата создания",
                                   nullable=True)  # user name

    other_contacts = NamedColumn(
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


class Ava(db.Model, Serializer):
    __tablename__ = 'ava'
    id = NamedColumn(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        nick='Id'
    )
    person_id = NamedColumn(
        db.Integer,
        MarkedForeignKey(Person.person_id),
        nick='человек',
        nullable=False,
        index=True,
    )
    ava = NamedColumn(
        db.Text,
        nick='картинка',
        nullable=False,
    )
    entry_state = NamedColumn(
        db.Text,
        nick='статус',
        nullable=False,
        index=True,
        default=EntryStates.RELEVANT
    )

    person = db.relationship('Person', lazy='noload', back_populates='avas')


class DirectLogin(db.Model, Serializer):
    __tablename__ = 'direct_login'
    type = NamedColumn(db.String,
                       nick='тип авторизации',
                       primary_key=True)
    person_id = NamedColumn(db.Integer,
                            MarkedForeignKey(Person.person_id),
                            nick='человек',
                            primary_key=True)
    login = NamedColumn(db.Text,
                        nick='логин',
                        nullable=False)
    password_hash = NamedColumn(db.Text,
                                nick='хэш пароля',
                                nullable=False)
    person = db.relationship('Person', lazy='joined')


class Contact(db.Model, Serializer):
    __tablename__ = 'contact'
    id = NamedColumn(db.Integer,
                     nick='id',
                     primary_key=True,
                     autoincrement=True)
    person_id = NamedColumn(
        db.Integer,
        MarkedForeignKey(Person.person_id),
        nick='человек',
        nullable=False
    )
    person = db.relationship(
        'Person',
        lazy='joined'
    )
    name = NamedColumn(
        db.Text,
        nick='название',
        nullable=False
    )
    value = NamedColumn(
        db.Text,
        nick='значение',
        nullable=False
    )


class School(db.Model, Serializer):
    __tablename__ = 'school'
    school_id = NamedColumn(db.Integer,
                            nick="id",
                            primary_key=True,
                            autoincrement=True)
    school_title = NamedColumn(db.Text,
                               nick="название",
                               nullable=False)
    school_type = NamedColumn(
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
    school_date_start = NamedColumn(
        db.Text,
        nick="дата начала",
        nullable=False
    )  # дата начала
    school_date_end = NamedColumn(
        db.Text,
        nick="дата конца",
        nullable=False
    )  # дата конца
    school_location = NamedColumn(
        db.Text,
        nick="место проведения",
        nullable=False
    )  # место проведения (2.7+)
    school_coords = NamedColumn(
        db.Text,
        nick="координаты проведения",
        nullable=False
    )  # координаты
    school_created = NamedColumn(
        db.Text,
        nick="дата создания",
        nullable=False
    )  # utc timestamp
    school_modified = NamedColumn(
        db.Text,
        nick="последнее изменение",
        nullable=False
    )  # utc timestamp
    school_changedby = NamedColumn(db.Text,
                                   nick="изменивший",
                                   nullable=False)  # user name
    person_comments = db.relationship('PersonComment', back_populates='school', lazy='dynamic')
    person_schools = db.relationship('PersonSchool', back_populates='school', lazy='dynamic')
    courses = db.relationship('Course', back_populates='school', lazy='dynamic')


class Course(db.Model, Serializer):
    __tablename__ = 'course'
    course_id = NamedColumn(db.Integer,
                            nick="id",
                            primary_key=True,
                            autoincrement=True)
    course_title = NamedColumn(db.Text,
                               nick="название",
                               nullable=False)  # название курса
    school_id = NamedColumn(db.Integer,
                            MarkedForeignKey(School.school_id),
                            nick="школа",
                            nullable=False)  # ссылка на школу, на которой читали курс
    school = db.relationship('School', lazy='joined')
    course_cycle = NamedColumn(db.Text,
                               nick="цикл",
                               nullable=True)  # цикл, на котором читался курс
    target_class = NamedColumn(db.Text,
                               nick="целевая аудитория",
                               nullable=True)  # диапазон классов, на которые рассчитан курс
    course_desc = NamedColumn(db.Text,
                              nick="описание",
                              nullable=True)  # описание курса
    course_type = NamedColumn(
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
    course_area = NamedColumn(
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
    course_comment = NamedColumn(db.Text,
                                 nick="комментарий",
                                 nullable=True)  # комментарий к курсу(чатик пока не делаем)
    course_created = NamedColumn(db.Text,
                                 nick="дата создания",
                                 nullable=False)  # utc timestamp
    course_modified = NamedColumn(db.Text,
                                  nick="последнее изменение",
                                  nullable=False)  # utc timestamp
    course_changedby = NamedColumn(db.Text,
                                   nick="изменивший",
                                   nullable=False)  # user name
    exams = db.relationship('Exam', back_populates='course', lazy='dynamic')
    course_teachers = db.relationship('CourseTeachers', back_populates='course', lazy='dynamic')


class CourseTeachers(db.Model, Serializer):
    __tablename__ = 'course_teachers'
    course_teachers_id = NamedColumn(db.Integer,
                                     nick="id",
                                     primary_key=True,
                                     autoincrement=True)
    course_id = NamedColumn(db.Integer,
                            MarkedForeignKey(Course.course_id),
                            nick="курс",
                            nullable=False)
    course = db.relationship('Course', lazy='joined')
    course_teacher_id = NamedColumn(db.Integer,
                                    MarkedForeignKey(Person.person_id),
                                    nick="перпод",
                                    nullable=False)
    course_teacher = db.relationship('Person', lazy='joined')
    course_teachers_created = NamedColumn(db.Text,
                                          nick="дата создания",
                                          nullable=False)  # utc timestampcourse_teacher
    course_teachers_modified = NamedColumn(db.Text,
                                           nick="последнее изменение",
                                           nullable=False)  # utc timestamp
    course_teachers_changedby = NamedColumn(db.Text,
                                            nick="изменивший",
                                            nullable=False)  # user name


class Exam(db.Model, Serializer):
    __tablename__ = 'exam'
    exam_id = NamedColumn(db.Integer,
                          nick="id",
                          primary_key=True,
                          autoincrement=True)  # not used
    student_person_id = NamedColumn(db.Integer,
                                    MarkedForeignKey(Person.person_id),
                                    nick="школьник",
                                    nullable=False)
    student = db.relationship('Person', lazy='joined')
    course_id = NamedColumn(db.Integer,
                            MarkedForeignKey(Course.course_id),
                            nick="курс",
                            nullable=False)
    course = db.relationship('Course', lazy='joined')
    exam_status = NamedColumn(db.Text,
                              nick="статус",
                              nullable=True)
    deadline_date = NamedColumn(db.Text,
                                nick="дедлайн",
                                nullable=True)
    exam_comment = NamedColumn(db.Text,
                               nick="комментарий",
                               nullable=True)
    exam_created = NamedColumn(db.Text,
                               nick="дата создания",
                               nullable=False)  # utc timestamp
    exam_modified = NamedColumn(db.Text,
                                nick="последнее изменение",
                                nullable=False)  # utc timestamp
    exam_changedby = NamedColumn(db.Text,
                                 nick="изменивший",
                                 nullable=False)  # user name


class PersonSchool(db.Model, Serializer):
    __tablename__ = 'person_school'
    person_school_id = NamedColumn(db.Integer,
                                   nick="id",
                                   primary_key=True,
                                   autoincrement=True)
    member_person_id = NamedColumn(db.Integer,
                                   MarkedForeignKey(Person.person_id),
                                   nick="участник",
                                   nullable=False)  # fk person
    member_person = db.relationship('Person', lazy='joined')
    member_department_id = NamedColumn(db.Integer,
                                       MarkedForeignKey(Department.department_id),
                                       nick="отделение",
                                       nullable=False)  # fk department
    department = db.relationship('Department', lazy='joined')
    school_id = NamedColumn(db.Integer,
                            MarkedForeignKey(School.school_id),
                            nick="школа",
                            nullable=False)  # fk school
    school = db.relationship('School', lazy='joined')
    is_student = NamedColumn(db.Text,
                             nick="школьник",
                             nullable=True)  # является ли школьником на данной школе
    is_teacher = NamedColumn(db.Text,
                             nick="препод",
                             nullable=True)  # является ли преподом на данной школе
    curatorship = NamedColumn(
        db.Enum(
            '',
            'none',
            'assist',
            'cur',
            name='curatorship_type'),
        nick="кураторство",
        nullable=True)  # кураторство на данной школе enum: (никто, помкур, куратор)
    curator_group = NamedColumn(db.Text,
                                nick="группа кураторства",
                                nullable=True)  # группа кураторства
    # класс, в котором находится школьник
    # (для Летней школы надо договориться, какой именно класс мы ставим, -- будущий или прошедший)
    current_class = NamedColumn(db.Text,
                                nick="класс",
                                nullable=True)
    courses_needed = NamedColumn(db.Text,
                                 nick="необходимое количество курсов",
                                 nullable=True)  # потребное кол - во курсов для сдачи на школе
    person_school_comment = NamedColumn(db.Text,
                                        nick="комментарий",
                                        nullable=True)  # комментарий(v2.10)
    person_school_created = NamedColumn(db.Text,
                                        nick="дата создания",
                                        nullable=False)  # utc timestamp
    person_school_modified = NamedColumn(db.Text,
                                         nick="последнее изменение",
                                         nullable=False)  # utc timestamp
    person_school_changedby = NamedColumn(db.Text,
                                          nick="изменивший",
                                          nullable=False)  # user name
    frm = NamedColumn(db.Text,
                      nick="заезд", )
    tll = NamedColumn(db.Text,
                      nick="отъезд", )

    calendars = db.relationship('Calendar', back_populates='person_school')


class Calendar(db.Model, Serializer):
    __tablename__ = 'calendar'

    person_school_id = NamedColumn(
        db.Integer,
        MarkedForeignKey(PersonSchool.person_school_id),
        nick="person_school",
        nullable=False,
        primary_key=True
    )
    person_school = db.relationship(PersonSchool)
    date = NamedColumn(
        db.DATE,
        nick="дата",
        nullable=False,
        primary_key=True
    )
    status = NamedColumn(
        db.Text,
        nick='статус',
        nullable=False)
    calendar_modified = NamedColumn(
        db.TIMESTAMP,
        nick='время',
        nullable=False,
    )
    changed_by = NamedColumn(
        db.Text,
        nick='изменивший',
        nullable=False
    )


class PersonComment(db.Model, Serializer):
    __tablename__ = 'person_comment'
    person_comment_id = NamedColumn(db.Integer,
                                    nick="id",
                                    primary_key=True,
                                    autoincrement=True)
    comment_text = NamedColumn(db.Text,
                               nick="комментарий",
                               nullable=True)  # текст комментария
    blamed_person_id = NamedColumn(db.Integer,
                                   MarkedForeignKey(Person.person_id),
                                   nick="упомянутый",
                                   nullable=False)  # fk person - - сабжевый участник(типично школьник)
    blamed_person = db.relationship('Person', lazy='joined')
    school_id = NamedColumn(db.Integer,
                            MarkedForeignKey(School.school_id),
                            nick="школа",
                            nullable=False)  # fk school - - школа, о которой идёт речь(v2.15)
    school = db.relationship('School', lazy='joined')
    owner_login = NamedColumn(db.Text,
                              nick="автор",
                              nullable=False)  # логин автора комментария
    record_acl = NamedColumn(db.Text,
                             nullable=True)  # ACL(v2.15)
    person_comment_created = NamedColumn(db.Text,
                                         nick="дата создания",
                                         nullable=False)  # utc timestamp
    person_comment_modified = NamedColumn(db.Text,
                                          nick="последние изменение",
                                          nullable=False)  # utc timestamp
    person_comment_deleted = NamedColumn(db.Text,
                                         nick="дата удаления",
                                         nullable=True)  # признак удаления(из базы ничего удалить нельзя)
    person_comment_changedby = NamedColumn(db.Text,
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
class Submission(db.Model, Serializer):
    __tablename__ = 'submission'
    submission_id = NamedColumn(db.Integer,
                                primary_key=True,
                                autoincrement=True)
    mail = NamedColumn(db.Text,
                       nullable=True)
    attachment = NamedColumn(db.Text,
                             nullable=True)
    fileexchange = NamedColumn(db.Text,
                               nullable=True)
    submission_timestamp = NamedColumn(db.Text,
                                       nullable=True)
    sender = NamedColumn(db.Text,
                         nullable=True)
    replied = NamedColumn(db.Text,
                          nullable=True)
    processed = NamedColumn(db.Text,
                            nullable=True)
    contest_year = NamedColumn(db.Text,
                               nullable=True)


class Contestants(db.Model, Serializer):
    __tablename__ = 'contestants'
    contestants_id = NamedColumn(db.Integer,
                                 primary_key=True,
                                 autoincrement=True)
    name = NamedColumn(db.Text,
                       nullable=True)
    mail = NamedColumn(db.Text,
                       nullable=True)
    phone = NamedColumn(db.Text,
                        nullable=True)
    parents = NamedColumn(db.Text,
                          nullable=True)
    address = NamedColumn(db.Text,
                          nullable=True)
    school = NamedColumn(db.Text,
                         nullable=True)
    level = NamedColumn(db.Text,
                        nullable=True)
    teacher_name = NamedColumn(db.Text,
                               nullable=True)
    work = NamedColumn(db.Text,
                       nullable=True)
    fileexchange = NamedColumn(db.Text,
                               nullable=True)
    status = NamedColumn(db.Text,
                         nullable=True)
    contest_year = NamedColumn(db.Text,
                               nullable=True)
    solutions = db.relationship('Solutions', back_populates='contestant', lazy='dynamic')


class Problems(db.Model, Serializer):
    __tablename__ = 'problems'
    problems_id = NamedColumn(db.Integer,
                              primary_key=True,
                              autoincrement=True)
    contest_year = NamedColumn(db.Text,
                               nullable=True)
    problem_name = NamedColumn(db.Text,
                               nullable=True)
    problem_html = NamedColumn(db.Text,
                               nullable=True)
    people = NamedColumn(db.Text,
                         nullable=True)
    criteria = NamedColumn(db.Text,
                           nullable=True)
    solutions = db.relationship('Solutions', back_populates='problem', lazy='dynamic')


class Solutions(db.Model, Serializer):
    __tablename__ = 'solutions'
    solutions_id = NamedColumn(db.Integer,
                               primary_key=True,
                               autoincrement=True)
    problem_id = NamedColumn(db.Integer,
                             MarkedForeignKey(Problems.problems_id),
                             nullable=False)
    problem = db.relationship('Problems', lazy='joined')
    contest_year = NamedColumn(db.Text,
                               nullable=True)
    contestant_id = NamedColumn(db.Integer,
                                MarkedForeignKey(Contestants.contestants_id),
                                nullable=False)
    contestant = db.relationship('Contestants', lazy='joined')
    resolution_text = NamedColumn(db.Text,
                                  nullable=True)
    resolution_author = NamedColumn(db.Text,
                                    nullable=True)
    resolution_mark = NamedColumn(db.Text,
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
