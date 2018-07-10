from flask_sqlalchemy import SQLAlchemy

"""
ORM declaration file
"""

db = SQLAlchemy()


class MarkedForeignKey(db.ForeignKey):

    def __init__(self, col, *args, **kwargs):
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
class Notification(db.Model):
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
class Department(db.Model):
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
    person_schools = db.relationship('PersonSchool', backref='department', lazy='dynamic')
    persons = db.relationship('Person', backref='department', lazy='dynamic')


class Person(db.Model):
    __tablename__ = 'person'
    person_id = NamedColumn(db.Integer,
                            nick="id",
                            primary_key=True,
                            autoincrement=True)
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

    person_created = NamedColumn(db.Text,
                                 nick="дата создания",
                                 nullable=True)  # utc timestamp
    person_modified = NamedColumn(db.Text,
                                  nick="последняя модификация",
                                  nullable=True)  # utc timestamp
    person_changedby = NamedColumn(db.Text,
                                   nick="дата создания",
                                   nullable=True)  # user name

    person_comments = db.relationship('PersonComment', backref='blamed_person', lazy='dynamic')
    person_schools = db.relationship('PersonSchool', backref='member_person', lazy='dynamic')
    exams = db.relationship('Exam', backref='student_person', lazy='dynamic')
    course_teachers = db.relationship('CourseTeachers', backref='course_teacher', lazy='dynamic')


class Course(db.Model):
    __tablename__ = 'course'
    course_id = NamedColumn(db.Integer,
                            nick="id",
                            primary_key=True,
                            autoincrement=True)
    course_title = NamedColumn(db.Text,
                               nick="название",
                               nullable=False)  # название курса
    school_id = NamedColumn(db.Integer,
                            nick="школа",
                            nullable=False)  # ссылка на школу, на которой читали курс
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
    exams = db.relationship('Exam', backref='course', lazy='dynamic')
    course_teachers = db.relationship('CourseTeachers', backref='course', lazy='dynamic')


class CourseTeachers(db.Model):
    __tablename__ = 'course_teachers'
    course_teachers_id = NamedColumn(db.Integer,
                                     nick="id",
                                     primary_key=True,
                                     autoincrement=True)
    course_id = NamedColumn(db.Integer,
                            MarkedForeignKey(Course.course_id),
                            nick="курс",
                            nullable=False)
    course_teacher_id = NamedColumn(db.Integer,
                                    MarkedForeignKey(Person.person_id),
                                    nick="перпод",
                                    nullable=False)
    course_teachers_created = NamedColumn(db.Text,
                                          nick="дата создания",
                                          nullable=False)  # utc timestamp
    course_teachers_modified = NamedColumn(db.Text,
                                           nick="последнее изменение",
                                           nullable=False)  # utc timestamp
    course_teachers_changedby = NamedColumn(db.Text,
                                            nick="изменивший",
                                            nullable=False)  # user name

    def teacher(self):
        return Person.query.get(self.course_teacher_id)

    def course(self):
        return Course.query.get(self.course_id)


class Exam(db.Model):
    __tablename__ = 'exam'
    exam_id = NamedColumn(db.Integer,
                          nick="id",
                          primary_key=True,
                          autoincrement=True)  # not used
    student_person_id = NamedColumn(db.Integer,
                                    MarkedForeignKey(Person.person_id),
                                    nick="школьник",
                                    nullable=False)
    course_id = NamedColumn(db.Integer,
                            MarkedForeignKey(Course.course_id),
                            nick="курс",
                            nullable=False)
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

    def student(self):
        return Person.query.get(self.student_person_id)

    def course(self):
        return Course.query.get(self.course_id)


class School(db.Model):
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
    school_date_start = NamedColumn(db.Text,
                                    nick="дата начала",
                                    nullable=False)  # дата начала
    school_date_end = NamedColumn(db.Text,
                                  nick="дата конца",
                                  nullable=False)  # дата конца
    school_location = NamedColumn(db.Text,
                                  nick="место проведения",
                                  nullable=False)  # место проведения (2.7+)
    school_created = NamedColumn(db.Text,
                                 nick="дата создания",
                                 nullable=False)  # utc timestamp
    school_modified = NamedColumn(db.Text,
                                  nick="последнее изменение",
                                  nullable=False)  # utc timestamp
    school_changedby = NamedColumn(db.Text,
                                   nick="изменивший",
                                   nullable=False)  # user name
    person_comments = db.relationship('PersonComment', backref='school', lazy='dynamic')
    person_schools = db.relationship('PersonSchool', backref='school', lazy='dynamic')


class PersonSchool(db.Model):
    __tablename__ = 'person_school'
    person_school_id = NamedColumn(db.Integer,
                                   nick="id",
                                   primary_key=True,
                                   autoincrement=True)
    member_person_id = NamedColumn(db.Integer,
                                   MarkedForeignKey(Person.person_id),
                                   nick="участник",
                                   nullable=False)  # fk person
    member_department_id = NamedColumn(db.Integer,
                                       MarkedForeignKey(Department.department_id),
                                       nick="отделение",
                                       nullable=False)  # fk department
    school_id = NamedColumn(db.Integer,
                            MarkedForeignKey(School.school_id),
                            nick="школа",
                            nullable=False)  # fk school
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
                      nick="заезд",)
    tll = NamedColumn(db.Text,
                      nick="отъезд", )


class PersonComment(db.Model):
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
    school_id = NamedColumn(db.Integer,
                            MarkedForeignKey(School.school_id),
                            nick="школа",
                            nullable=False)  # fk school - - школа, о которой идёт речь(v2.15)
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


# contest TODO: nickname columns
class Submission(db.Model):
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


class Contestants(db.Model):
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
    solutions = db.relationship('Solutions', backref='contestant', lazy='dynamic')


class Problems(db.Model):
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
    solutions = db.relationship('Solutions', backref='problem', lazy='dynamic')


class Solutions(db.Model):
    __tablename__ = 'solutions'
    solutions_id = NamedColumn(db.Integer,
                               primary_key=True,
                               autoincrement=True)
    problem_id = NamedColumn(db.Integer,
                             MarkedForeignKey(Problems.problems_id),
                             nullable=False)
    contest_year = NamedColumn(db.Text,
                               nullable=True)
    contestant_id = NamedColumn(db.Integer,
                                MarkedForeignKey(Contestants.contestants_id),
                                nullable=False)
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
