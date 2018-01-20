from flask_sqlalchemy import SQLAlchemy
import yasm.config as cfg


# for autocomplete
# notification
Notification = None
# *SM
Department = None
Person = None
Course = None
CourseTeachers = None
Exam = None
School = None
PersonSchool = None
PersonComment = None
# contest
Submission = None
Contestants = None
Problems = None
Solutions = None


def connect(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = cfg.db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    database = SQLAlchemy(app)

    # notification
    class ModelNotification(database.Model):
        __tablename__ = 'notification'
        notification_id = database.Column(database.Integer, primary_key=True, autoincrement=True)
        mail_group = database.Column(database.Text, nullable=False)
        notification_text = database.Column(database.Text, nullable=False)
        notification_html = database.Column(database.Text, nullable=False)
    global Notification
    Notification = ModelNotification

    # XSM
    class ModelDepartment(database.Model):
        __tablename__ = 'department'
        department_id = database.Column(database.Integer, primary_key=True, autoincrement=True)
        department_title = database.Column(database.Text, nullable=False)
        department_created = database.Column(database.Text, nullable=False)
        department_modified = database.Column(database.Text, nullable=False)
        department_changedby = database.Column(database.Text, nullable=False)
    global Department
    Department = ModelDepartment

    class ModelPerson(database.Model):
        __tablename__ = 'person'
        person_id = database.Column(database.Integer, primary_key=True, autoincrement=True)
        last_name = database.Column(database.Text, nullable=False) # фамилия
        first_name = database.Column(database.Text, nullable=False)  # имя
        patronymic = database.Column(database.Text, nullable=True)  # отчество
        nick_name = database.Column(database.Text, nullable=True)  # кличка #569

        birth_date = database.Column(database.Text, nullable=False)  # дата рождения
        passport_data = database.Column(database.Text, nullable=False)  # паспортные данные

        school = database.Column(database.Text, nullable=False)  # школа, в которой учится школьник
        school_city = database.Column(database.Text, nullable=False)  # город, в котором находится школа
        ank_class = database.Column(database.Text, nullable=False)  # класс подачи заявки
        current_class = database.Column(database.Text, nullable=False)  # текущий класс

        phone = database.Column(database.Text, nullable=True)  # телефон (городской)
        cellular = database.Column(database.Text, nullable=True)  # мобильный телефон
        email = database.Column(database.Text, nullable=True)  # контактный email
        skype = database.Column(database.Text, nullable=True)  # skype
        social_profile = database.Column(database.Text, nullable=True)  # профиль ВКонтакте и т.п. (используемый!)

        is_teacher = database.Column(database.Text, nullable=True)  # типично препод
        is_student = database.Column(database.Text, nullable=True)  # типично школьник

        favourites = database.Column(database.Text, nullable=True)  # любимые предметы
        achievements = database.Column(database.Text, nullable=True) # достижения
        hobby = database.Column(database.Text, nullable=True)  # хобби

        lesh_ref = database.Column(database.Text, nullable=True)  # откуда узнали о школе (2.1+)

        forest_1 = database.Column(database.Text, nullable=True)  # 1-й выход в лес (2.3a+)
        forest_2 = database.Column(database.Text, nullable=True)  # 2-й выход в лес (2.3a+)
        forest_3 = database.Column(database.Text, nullable=True)  # 3-й выход в лес (2.3a+)

        tent_capacity = database.Column(database.Text, nullable=True)  # количество мест в палатке (0 = палатки нет) (2.2+)
        tour_requisites =database.Column(database.Text, nullable=True)  # имеющиеся предметы туристского обихода (2.2+)

        anketa_status = database.Column(database.Enum('progress', 'nextyear', 'duplicate', 'reserved', 'cont', 'old', 'new', 'processed', 'declined', 'taken', 'duplicated', 'spam'), nullable=False)

        user_agent = database.Column(database.Text, nullable=True)  # идентификатор браузера, с которого была подана анкета

        department_id = database.Column(database.Integer, database.ForeignKey(Department.department_id), nullable=False)  # ссылка на отделение(2.7 +)

        person_created = database.Column(database.Text, nullable=True)  # utc timestamp
        person_modified = database.Column(database.Text, nullable=True)  # utc timestamp
        person_changedby = database.Column(database.Text, nullable=True)  # user name

        def department(self):
            return ModelDepartment.query.get(self.department_id)
    global Person
    Person = ModelPerson

    class ModelCourse(database.Model):
        __tablename__ = 'course'
        course_id = database.Column(database.Integer, primary_key=True, autoincrement=True)
        course_title = database.Column(database.Text, nullable=False)  # название курса
        school_id = database.Column(database.Integer, nullable=False)  # ссылка на школу, на которой читали курс
        course_cycle = database.Column(database.Text, nullable=True)  # цикл, на котором читался курс
        target_class = database.Column(database.Text, nullable=True)  # диапазон классов, на которые рассчитан курс
        course_desc = database.Column(database.Text, nullable=True)  # описание курса
        course_type = database.Column(database.Enum('generic', 'other', 'facult', 'prac', 'single'), nullable=False)  # тип курса(прак, поход, etc)
        course_area = database.Column(database.Enum('cs', 'unknown', 'nature', 'precise', 'other', 'human'), nullable=False)  # предметная область
        course_comment = database.Column(database.Text, nullable=True)  # комментарий к курсу(чатик пока не делаем)
        course_created = database.Column(database.Text, nullable=False) # utc timestamp
        course_modified = database.Column(database.Text, nullable=False) # utc timestamp
        course_changedby = database.Column(database.Text, nullable=False) # user name
    global Course
    Course = ModelCourse

    class ModelCourseTeachers(database.Model):
        __tablename__ = 'course_teachers'
        course_teachers_id = database.Column(database.Integer, primary_key=True, autoincrement=True)
        course_id = database.Column(database.Integer, database.ForeignKey(Course.course_id), nullable=False)
        course_teacher_id = database.Column(database.Integer, database.ForeignKey(Person.person_id), nullable=False)
        course_teachers_created = database.Column(database.Text, nullable=False) # utc timestamp
        course_teachers_modified  = database.Column(database.Text, nullable=False) # utc timestamp
        course_teachers_changedby = database.Column(database.Text, nullable=False) # user name

        def teacher(self):
            return Person.query.get(self.course_teacher_id)

        def course(self):
            return Course.query.get(self.course_id)
    global CourseTeachers
    CourseTeachers = ModelCourseTeachers

    class ModelExam(database.Model):
        __tablename__ = 'exam'
        exam_id = database.Column(database.Integer, primary_key=True, autoincrement=True)  # not used
        student_person_id = database.Column(database.Integer, database.ForeignKey(Person.person_id), nullable=False)
        course_id = database.Column(database.Integer, database.ForeignKey(Course.course_id), nullable=False)
        exam_status = database.Column(database.Text, nullable=True)
        deadline_date = database.Column(database.Text, nullable=True)
        exam_comment = database.Column(database.Text, nullable=True)
        exam_created = database.Column(database.Text, nullable=False)  # utc timestamp
        exam_modified = database.Column(database.Text, nullable=False)  # utc timestamp
        exam_changedby = database.Column(database.Text, nullable=False) # user name

        def student(self):
            return Person.query.get(self.student_person_id)

        def course(self):
            return Course.query.get(self.course_id)
    global Exam
    Exam = ModelExam

    class ModelSchool(database.Model):
        __tablename__ = 'school'
        school_id = database.Column(database.Integer, primary_key=True, autoincrement=True)
        school_title = database.Column(database.Text, nullable=False)
        school_type = database.Column(database.Enum('lesh', 'vesh', 'zesh', 'summer', 'summmer', 'winter', 'spring'), nullable=False)  # enum:(летняя, зимняя, весенняя) TODO: simplify
        school_date_start = database.Column(database.Text, nullable=False)  # дата начала
        school_date_end = database.Column(database.Text, nullable=False)  # дата конца
        school_location = database.Column(database.Text, nullable=False)  # место проведения (2.7+)
        school_created = database.Column(database.Text, nullable=False)  # utc timestamp
        school_modified = database.Column(database.Text, nullable=False)  # utc timestamp
        school_changedby = database.Column(database.Text, nullable=False)  # user name
    global School
    School = ModelSchool

    class ModelPersonSchool(database.Model):
        __tablename__ = 'person_school'
        person_school_id = database.Column(database.Integer, primary_key=True, autoincrement=True)
        member_person_id = database.Column(database.Integer, database.ForeignKey(Person.person_id), nullable=False)  # fk person
        member_department_id = database.Column(database.Integer, database.ForeignKey(Department.department_id), nullable=False)  # fk department
        school_id = database.Column(database.Integer, database.ForeignKey(School.school_id), nullable=False)  # fk school
        is_student = database.Column(database.Text, nullable=True)  # является ли школьником на данной школе
        is_teacher = database.Column(database.Text, nullable=True)  # является ли преподом на данной школе
        curatorship = database.Column(database.Enum('', 'none', 'assist', 'cur'))  # кураторство на данной школе enum: (никто, помкур, куратор)
        curator_group = database.Column(database.Text, nullable=True)  # группа кураторства
        current_class = database.Column(database.Text, nullable=True)  # класс, в котором находится школьник - - (для Летней школы надо договориться, какой именно класс мы ставим, -- будущий или прошедший
        courses_needed = database.Column(database.Text, nullable=True)  # потребное кол - во курсов для сдачи на школе
        person_school_comment = database.Column(database.Text, nullable=True)  # комментарий(v2.10)
        person_school_created = database.Column(database.Text, nullable=False)  # utc timestamp
        person_school_modified = database.Column(database.Text, nullable=False)  # utc timestamp
        person_school_changedby = database.Column(database.Text, nullable=False)  # user name
    global PersonSchool
    PersonSchool = ModelPersonSchool

    class ModelPersonComment(database.Model):
        __tablename__ = 'person_comment'
        person_comment_id = database.Column(database.Integer, primary_key=True, autoincrement=True)
        comment_text = database.Column(database.Text, nullable=True)  # текст комментария
        blamed_person_id = database.Column(database.Integer, database.ForeignKey(Person.person_id), nullable=False)  # fk person - - сабжевый участник(типично школьник)
        school_id = database.Column(database.Integer, database.ForeignKey(School.school_id), nullable=False)  # fk school - - школа, о которой идёт речь(v2.15)
        owner_login = database.Column(database.Text, nullable=False)  # логин автора комментария
        record_acl = database.Column(database.Text, nullable=True)  # ACL(v2.15)
        person_comment_created = database.Column(database.Text, nullable=False)  # utc timestamp
        person_comment_modified = database.Column(database.Text, nullable=False)  # utc timestamp
        person_comment_deleted = database.Column(database.Text, nullable=True)  # признак удаления(из базы ничего удалить нельзя)
        person_comment_changedby = database.Column(database.Text, nullable=False)  # user name
    global PersonComment
    PersonComment = ModelPersonComment

    # contest
    class ModelSubmission(database.Model):
        __tablename__ = 'submission'
        submission_id = database.Column(database.Integer, primary_key=True, autoincrement=True)
        mail = database.Column(database.Text, nullable=True)
        attachment = database.Column(database.Text, nullable=True)
        fileexchange = database.Column(database.Text, nullable=True)
        submission_timestamp = database.Column(database.Text, nullable=True)
        sender = database.Column(database.Text, nullable=True)
        replied = database.Column(database.Text, nullable=True)
        processed = database.Column(database.Text, nullable=True)
        contest_year = database.Column(database.Text, nullable=True)
    global Submission
    Submission = ModelSubmission

    class ModelContestants(database.Model):
        __tablename__ = 'contestants' 
        contestants_id = database.Column(database.Integer, primary_key=True, autoincrement=True)
        name = database.Column(database.Text, nullable=True)
        mail = database.Column(database.Text, nullable=True)
        phone = database.Column(database.Text, nullable=True)
        parents = database.Column(database.Text, nullable=True)
        address = database.Column(database.Text, nullable=True)
        school = database.Column(database.Text, nullable=True)
        level = database.Column(database.Text, nullable=True)
        teacher_name = database.Column(database.Text, nullable=True)
        work = database.Column(database.Text, nullable=True)
        fileexchange = database.Column(database.Text, nullable=True)
        status = database.Column(database.Text, nullable=True)
        contest_year = database.Column(database.Text, nullable=True)
    global Contestants
    Contestants = ModelContestants

    class ModelProblems(database.Model):
        __tablename__ = 'problems'
        problems_id = database.Column(database.Integer, primary_key=True, autoincrement=True)
        contest_year = database.Column(database.Text, nullable=True)
        problem_name = database.Column(database.Text, nullable=True)
        problem_html = database.Column(database.Text, nullable=True)
        people = database.Column(database.Text, nullable=True)
        criteria = database.Column(database.Text, nullable=True)
    global Problems
    Problems = ModelProblems

    class ModelSolutions(database.Model):
        __tablename__ = 'solutions'
        solutions_id = database.Column(database.Integer, primary_key=True, autoincrement=True)
        problem_id = database.Column(database.Integer, database.ForeignKey(Problems.problems_id), nullable=False)
        contest_year = database.Column(database.Text, nullable=True)
        contestant_id = database.Column(database.Integer, database.ForeignKey(Contestants.contestants_id), nullable=False)
        resolution_text = database.Column(database.Text, nullable=True)
        resolution_author = database.Column(database.Text, nullable=True)
        resolution_mark = database.Column(database.Text, nullable=True)
    global Solutions
    Solutions = ModelSolutions

    return app, database