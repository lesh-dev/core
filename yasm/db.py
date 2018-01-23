from flask_sqlalchemy import SQLAlchemy
"""
ORM declaration file
"""


database = SQLAlchemy()


class NamedColumn(database.Column):
    """
    Wrapper around SQLAlchemy.Column, which allows giving nicknames to columns.
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
class Notification(database.Model):
    __tablename__ = 'notification'
    notification_id = NamedColumn(database.Integer,
                                  nick="id",
                                  primary_key=True,
                                  autoincrement=True)
    mail_group = NamedColumn(database.Text,
                             nick="группа",
                             nullable=False)
    notification_text = NamedColumn(database.Text,
                                    nick="текст",
                                    nullable=False)
    notification_html = NamedColumn(database.Text,
                                    nick="html",
                                    nullable=False)


# XSM
class Department(database.Model):
    __tablename__ = 'department'
    department_id = NamedColumn(database.Integer,
                                nick="id",
                                primary_key=True,
                                autoincrement=True)
    department_title = NamedColumn(database.Text,
                                   nick="название",
                                   nullable=False)
    department_created = NamedColumn(database.Text,
                                     nick="дата создания",
                                     nullable=False)
    department_modified = NamedColumn(database.Text,
                                      nick="последняя модификация",
                                      nullable=False)
    department_changedby = NamedColumn(database.Text,
                                       nick="изменивший",
                                       nullable=False)


class Person(database.Model):
    __tablename__ = 'person'
    person_id = NamedColumn(database.Integer,
                            nick="id",
                            primary_key=True,
                            autoincrement=True)
    last_name = NamedColumn(database.Text,
                            nick="фамилия",
                            nullable=False)  # фамилия
    first_name = NamedColumn(database.Text,
                             nick="имя",
                             nullable=False)  # имя
    patronymic = NamedColumn(database.Text,
                             nick="отчество",
                             nullable=True)  # отчество
    nick_name = NamedColumn(database.Text,
                            nick="прозвище",
                            nullable=True)  # кличка #569

    birth_date = NamedColumn(database.Text,
                             nick="дата рождения",
                             nullable=False)  # дата рождения
    passport_data = NamedColumn(database.Text,
                                nick="паспортные данные",
                                nullable=False)  # паспортные данные

    school = NamedColumn(database.Text,
                         nick="школа",
                         nullable=False)  # школа, в которой учится школьник
    school_city = NamedColumn(database.Text,
                              nick="город",
                              nullable=False)  # город, в котором находится школа
    ank_class = NamedColumn(database.Text,
                            nick="класс подачи заявки",
                            nullable=False)  # класс подачи заявки
    current_class = NamedColumn(database.Text,
                                nick="текущий класс",
                                nullable=False)  # текущий класс

    phone = NamedColumn(database.Text,
                        nick="городской",
                        nullable=True)  # телефон (городской)
    cellular = NamedColumn(database.Text,
                           nick="мобильный",
                           nullable=True)  # мобильный телефон
    email = NamedColumn(database.Text,
                        nullable=True)  # контактный email
    skype = NamedColumn(database.Text,
                        nullable=True)  # skype
    social_profile = NamedColumn(database.Text,
                                 nick="профиль в соц. сети",
                                 nullable=True)  # профиль ВКонтакте и т.п. (используемый!)

    is_teacher = NamedColumn(database.Text,
                             nick="препод",
                             nullable=True)  # типично препод
    is_student = NamedColumn(database.Text,
                             nick="школьник",
                             nullable=True)  # типично школьник

    favourites = NamedColumn(database.Text,
                             nick="любимые предметы",
                             nullable=True)  # любимые предметы
    achievements = NamedColumn(database.Text,
                               nick="достижения",
                               nullable=True)  # достижения
    hobby = NamedColumn(database.Text,
                        nick="хобби",
                        nullable=True)  # хобби

    lesh_ref = NamedColumn(database.Text,
                           nick="откуда узнал",
                           nullable=True)  # откуда узнали о школе (2.1+)

    forest_1 = NamedColumn(database.Text,
                           nick="1-й выход в лес",
                           nullable=True)  # 1-й выход в лес (2.3a+)
    forest_2 = NamedColumn(database.Text,
                           nick="2-й выход в лес",
                           nullable=True)  # 2-й выход в лес (2.3a+)
    forest_3 = NamedColumn(database.Text,
                           nick="3-й выход в лес",
                           nullable=True)  # 3-й выход в лес (2.3a+)

    tent_capacity = NamedColumn(database.Text,
                                nick="мест в палатке",
                                nullable=True)  # количество мест в палатке (0 = палатки нет) (2.2+)
    tour_requisites = NamedColumn(database.Text,
                                  nick="тур. инвентарь",
                                  nullable=True)  # имеющиеся предметы туристского обихода (2.2+)

    anketa_status = NamedColumn(database.Enum('progress',
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
                                              'spam'),
                                nick="статус анкеты",
                                nullable=False)

    user_agent = NamedColumn(database.Text,
                             nick="браузер",
                             nullable=True)  # идентификатор браузера, с которого была подана анкета

    department_id = NamedColumn(database.Integer,
                                database.ForeignKey(Department.department_id),
                                nick="отделение",
                                nullable=False)  # ссылка на отделение(2.7 +)

    person_created = NamedColumn(database.Text,
                                 nick="дата создания",
                                 nullable=True)  # utc timestamp
    person_modified = NamedColumn(database.Text,
                                  nick="последняя модификация",
                                  nullable=True)  # utc timestamp
    person_changedby = NamedColumn(database.Text,
                                   nick="дата создания",
                                   nullable=True)  # user name

    def department(self):
        return Department.query.get(self.department_id)


class Course(database.Model):
    __tablename__ = 'course'
    course_id = NamedColumn(database.Integer,
                            nick="id",
                            primary_key=True,
                            autoincrement=True)
    course_title = NamedColumn(database.Text,
                               nick="название",
                               nullable=False)  # название курса
    school_id = NamedColumn(database.Integer,
                            nick="школа",
                            nullable=False)  # ссылка на школу, на которой читали курс
    course_cycle = NamedColumn(database.Text,
                               nick="цикл",
                               nullable=True)  # цикл, на котором читался курс
    target_class = NamedColumn(database.Text,
                               nick="целевая аудитория",
                               nullable=True)  # диапазон классов, на которые рассчитан курс
    course_desc = NamedColumn(database.Text,
                              nick="описание",
                              nullable=True)  # описание курса
    course_type = NamedColumn(database.Enum('generic',
                                            'other',
                                            'facult',
                                            'prac',
                                            'single'),
                              nick="тип",
                              nullable=False)  # тип курса(прак, поход, etc)
    course_area = NamedColumn(database.Enum('cs',
                                            'unknown',
                                            'nature',
                                            'precise',
                                            'other',
                                            'human'),
                              nick="область",
                              nullable=False)  # предметная область
    course_comment = NamedColumn(database.Text,
                                 nick="комментарий",
                                 nullable=True)  # комментарий к курсу(чатик пока не делаем)
    course_created = NamedColumn(database.Text,
                                 nick="дата создания",
                                 nullable=False)  # utc timestamp
    course_modified = NamedColumn(database.Text,
                                  nick="последнее изменение",
                                  nullable=False)  # utc timestamp
    course_changedby = NamedColumn(database.Text,
                                   nick="изменивший",
                                   nullable=False)  # user name


class CourseTeachers(database.Model):
    __tablename__ = 'course_teachers'
    course_teachers_id = NamedColumn(database.Integer,
                                     nick="id",
                                     primary_key=True,
                                     autoincrement=True)
    course_id = NamedColumn(database.Integer,
                            database.ForeignKey(Course.course_id),
                            nick="курс",
                            nullable=False)
    course_teacher_id = NamedColumn(database.Integer,
                                    database.ForeignKey(Person.person_id),
                                    nick="перпод",
                                    nullable=False)
    course_teachers_created = NamedColumn(database.Text,
                                          nick="дата создания",
                                          nullable=False)  # utc timestamp
    course_teachers_modified = NamedColumn(database.Text,
                                           nick="последнее изменение",
                                           nullable=False)  # utc timestamp
    course_teachers_changedby = NamedColumn(database.Text,
                                            nick="изменивший",
                                            nullable=False)  # user name

    def teacher(self):
        return Person.query.get(self.course_teacher_id)

    def course(self):
        return Course.query.get(self.course_id)


class Exam(database.Model):
    __tablename__ = 'exam'
    exam_id = NamedColumn(database.Integer,
                          nick="id",
                          primary_key=True,
                          autoincrement=True)  # not used
    student_person_id = NamedColumn(database.Integer,
                                    database.ForeignKey(Person.person_id),
                                    nick="школьник",
                                    nullable=False)
    course_id = NamedColumn(database.Integer,
                            database.ForeignKey(Course.course_id),
                            nick="курс",
                            nullable=False)
    exam_status = NamedColumn(database.Text,
                              nick="статус",
                              nullable=True)
    deadline_date = NamedColumn(database.Text,
                                nick="дедлайн", 
                                nullable=True)
    exam_comment = NamedColumn(database.Text, 
                               nick="комментарий",
                               nullable=True)
    exam_created = NamedColumn(database.Text,
                               nick="дата создания",
                               nullable=False)  # utc timestamp
    exam_modified = NamedColumn(database.Text, 
                                nick="последнее изменение",
                                nullable=False)  # utc timestamp
    exam_changedby = NamedColumn(database.Text, 
                                 nick="изменивший", 
                                 nullable=False)  # user name

    def student(self):
        return Person.query.get(self.student_person_id)

    def course(self):
        return Course.query.get(self.course_id)


class School(database.Model):
    __tablename__ = 'school'
    school_id = NamedColumn(database.Integer,
                            nick="id",
                            primary_key=True,
                            autoincrement=True)
    school_title = NamedColumn(database.Text,
                               nick="название",
                               nullable=False)
    school_type = NamedColumn(database.Enum('lesh',
                                            'vesh',
                                            'zesh',
                                            'summer',
                                            'summmer',
                                            'winter',
                                            'spring'),
                              nick="тип",
                              nullable=False)  # enum:(летняя, зимняя, весенняя) TODO: simplify
    school_date_start = NamedColumn(database.Text,
                                    nick="дата начала",
                                    nullable=False)  # дата начала
    school_date_end = NamedColumn(database.Text,
                                  nick="дата конца",
                                  nullable=False)  # дата конца
    school_location = NamedColumn(database.Text,
                                  nick="место проведения",
                                  nullable=False)  # место проведения (2.7+)
    school_created = NamedColumn(database.Text,
                                 nick="дата создания",
                                 nullable=False)  # utc timestamp
    school_modified = NamedColumn(database.Text,
                                  nick="последнее изменение",
                                  nullable=False)  # utc timestamp
    school_changedby = NamedColumn(database.Text,
                                   nick="изменивший",
                                   nullable=False)  # user name


class PersonSchool(database.Model):
    __tablename__ = 'person_school'
    person_school_id = NamedColumn(database.Integer,
                                   nick="id",
                                   primary_key=True,
                                   autoincrement=True)
    member_person_id = NamedColumn(database.Integer,
                                   database.ForeignKey(Person.person_id),
                                   nick="участник",
                                   nullable=False)  # fk person
    member_department_id = NamedColumn(database.Integer,
                                       database.ForeignKey(Department.department_id),
                                       nick="отделение",
                                       nullable=False)  # fk department
    school_id = NamedColumn(database.Integer,
                            database.ForeignKey(School.school_id),
                            nick="школа",
                            nullable=False)  # fk school
    is_student = NamedColumn(database.Text,
                             nick="школьник",
                             nullable=True)  # является ли школьником на данной школе
    is_teacher = NamedColumn(database.Text,
                             nick="препод",
                             nullable=True)  # является ли преподом на данной школе
    curatorship = NamedColumn(database.Enum('',
                                            'none',
                                            'assist',
                                            'cur'),
                              nick="кураторство",
                              nullable=True)  # кураторство на данной школе enum: (никто, помкур, куратор)
    curator_group = NamedColumn(database.Text,
                                nick="группа кураторства",
                                nullable=True)  # группа кураторства
    # класс, в котором находится школьник
    # (для Летней школы надо договориться, какой именно класс мы ставим, -- будущий или прошедший)
    current_class = NamedColumn(database.Text,
                                nick="класс",
                                nullable=True)
    courses_needed = NamedColumn(database.Text,
                                 nick="необходимое количество курсов",
                                 nullable=True)  # потребное кол - во курсов для сдачи на школе
    person_school_comment = NamedColumn(database.Text,
                                        nick="комментарий",
                                        nullable=True)  # комментарий(v2.10)
    person_school_created = NamedColumn(database.Text,
                                        nick="дата создания",
                                        nullable=False)  # utc timestamp
    person_school_modified = NamedColumn(database.Text,
                                         nick="последнее изменение",
                                         nullable=False)  # utc timestamp
    person_school_changedby = NamedColumn(database.Text,
                                          nick="изменивший",
                                          nullable=False)  # user name


class PersonComment(database.Model):
    __tablename__ = 'person_comment'
    person_comment_id = NamedColumn(database.Integer,
                                    nick="id",
                                    primary_key=True,
                                    autoincrement=True)
    comment_text = NamedColumn(database.Text,
                               nick="комментарий",
                               nullable=True)  # текст комментария
    blamed_person_id = NamedColumn(database.Integer,
                                   database.ForeignKey(Person.person_id),
                                   nick="упомянутый",
                                   nullable=False)  # fk person - - сабжевый участник(типично школьник)
    school_id = NamedColumn(database.Integer,
                            database.ForeignKey(School.school_id),
                            nick="школа",
                            nullable=False)  # fk school - - школа, о которой идёт речь(v2.15)
    owner_login = NamedColumn(database.Text,
                              nick="автор",
                              nullable=False)  # логин автора комментария
    record_acl = NamedColumn(database.Text,
                             nullable=True)  # ACL(v2.15)
    person_comment_created = NamedColumn(database.Text,
                                         nick="дата создания",
                                         nullable=False)  # utc timestamp
    person_comment_modified = NamedColumn(database.Text,
                                          nick="последние изменение",
                                          nullable=False)  # utc timestamp
    person_comment_deleted = NamedColumn(database.Text,
                                         nick="дата удаления",
                                         nullable=True)  # признак удаления(из базы ничего удалить нельзя)
    person_comment_changedby = NamedColumn(database.Text,
                                           nick="изменивший",
                                           nullable=False)  # user name


# contest TODO: nickname columns
class Submission(database.Model):
    __tablename__ = 'submission'
    submission_id = NamedColumn(database.Integer,
                                primary_key=True,
                                autoincrement=True)
    mail = NamedColumn(database.Text,
                       nullable=True)
    attachment = NamedColumn(database.Text,
                             nullable=True)
    fileexchange = NamedColumn(database.Text,
                               nullable=True)
    submission_timestamp = NamedColumn(database.Text,
                                       nullable=True)
    sender = NamedColumn(database.Text,
                         nullable=True)
    replied = NamedColumn(database.Text,
                          nullable=True)
    processed = NamedColumn(database.Text,
                            nullable=True)
    contest_year = NamedColumn(database.Text,
                               nullable=True)


class Contestants(database.Model):
    __tablename__ = 'contestants'
    contestants_id = NamedColumn(database.Integer,
                                 primary_key=True,
                                 autoincrement=True)
    name = NamedColumn(database.Text,
                       nullable=True)
    mail = NamedColumn(database.Text,
                       nullable=True)
    phone = NamedColumn(database.Text,
                        nullable=True)
    parents = NamedColumn(database.Text,
                          nullable=True)
    address = NamedColumn(database.Text,
                          nullable=True)
    school = NamedColumn(database.Text,
                         nullable=True)
    level = NamedColumn(database.Text,
                        nullable=True)
    teacher_name = NamedColumn(database.Text,
                               nullable=True)
    work = NamedColumn(database.Text,
                       nullable=True)
    fileexchange = NamedColumn(database.Text,
                               nullable=True)
    status = NamedColumn(database.Text,
                         nullable=True)
    contest_year = NamedColumn(database.Text,
                               nullable=True)


class Problems(database.Model):
    __tablename__ = 'problems'
    problems_id = NamedColumn(database.Integer,
                              primary_key=True,
                              autoincrement=True)
    contest_year = NamedColumn(database.Text,
                               nullable=True)
    problem_name = NamedColumn(database.Text,
                               nullable=True)
    problem_html = NamedColumn(database.Text,
                               nullable=True)
    people = NamedColumn(database.Text,
                         nullable=True)
    criteria = NamedColumn(database.Text,
                           nullable=True)


class Solutions(database.Model):
    __tablename__ = 'solutions'
    solutions_id = NamedColumn(database.Integer,
                               primary_key=True,
                               autoincrement=True)
    problem_id = NamedColumn(database.Integer,
                             database.ForeignKey(Problems.problems_id),
                             nullable=False)
    contest_year = NamedColumn(database.Text,
                               nullable=True)
    contestant_id = NamedColumn(database.Integer,
                                database.ForeignKey(Contestants.contestants_id),
                                nullable=False)
    resolution_text = NamedColumn(database.Text,
                                  nullable=True)
    resolution_author = NamedColumn(database.Text,
                                    nullable=True)
    resolution_mark = NamedColumn(database.Text,
                                  nullable=True)


def db_read_test():
    """
    Checks if all items stored in database are readable by this ORM
    :return: None
    """
    for i in (Notification,
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
              Solutions):
        print(i.query.all())