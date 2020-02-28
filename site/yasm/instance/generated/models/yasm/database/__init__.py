import json
import sqlalchemy
import datetime
from flask_login import UserMixin

from ... import stub
from ... import yasm
from .... import enums



@stub.add_search
class Person(
        stub.db.Model,        UserMixin,    ):
    __tablename__ = 'person'

    def __init__(self, *args, **kwargs):
        self.serialized = False
        super(Person, self).__init__(*args, **kwargs)

    @sqlalchemy.orm.reconstructor
    def init_on_load(self):
        self.serialized = False
    def get_id(self):
        return tuple(
            id,
        )

    id = stub.db.Column(
        stub.db.Integer,
        name='person_id',
        primary_key=True,
        autoincrement=True,

    )
    rights = stub.db.Column(
        stub.db.Text,
        name='rights',
        nullable=True,

    )
    first_name = stub.db.Column(
        stub.db.Text,
        name='first_name',
        
    )
    last_name = stub.db.Column(
        stub.db.Text,
        name='last_name',
        
    )
    patronymic = stub.db.Column(
        stub.db.Text,
        name='patronymic',
        nullable=True,

    )
    nick_name = stub.db.Column(
        stub.db.Text,
        name='nick_name',
        nullable=True,

    )
    birth_date = stub.db.Column(
        stub.db.Text,
        name='birth_date',
        
    )
    passport_data = stub.db.Column(
        stub.db.Text,
        name='passport_data',
        
    )
    school = stub.db.Column(
        stub.db.Text,
        name='school',
        
    )
    school_city = stub.db.Column(
        stub.db.Text,
        name='school_city',
        
    )
    ank_class = stub.db.Column(
        stub.db.Text,
        name='ank_class',
        
    )
    current_class = stub.db.Column(
        stub.db.Text,
        name='current_class',
        
    )
    phone = stub.db.Column(
        stub.db.Text,
        name='phone',
        nullable=True,

    )
    cellular = stub.db.Column(
        stub.db.Text,
        name='cellular',
        nullable=True,

    )
    email = stub.db.Column(
        stub.db.Text,
        name='email',
        nullable=True,

    )
    skype = stub.db.Column(
        stub.db.Text,
        name='skype',
        nullable=True,

    )
    social_profile = stub.db.Column(
        stub.db.Text,
        name='social_profile',
        nullable=True,

    )
    is_teacher = stub.db.Column(
        stub.db.Text,
        name='is_teacher',
        nullable=True,

    )
    is_student = stub.db.Column(
        stub.db.Text,
        name='is_student',
        nullable=True,

    )
    favourites = stub.db.Column(
        stub.db.Text,
        name='favourites',
        nullable=True,

    )
    achievements = stub.db.Column(
        stub.db.Text,
        name='achievements',
        nullable=True,

    )
    hobby = stub.db.Column(
        stub.db.Text,
        name='hobby',
        nullable=True,

    )
    lesh_ref = stub.db.Column(
        stub.db.Text,
        name='lesh_ref',
        nullable=True,

    )
    forest_1 = stub.db.Column(
        stub.db.Text,
        name='forest_1',
        nullable=True,

    )
    forest_2 = stub.db.Column(
        stub.db.Text,
        name='forest_2',
        nullable=True,

    )
    forest_3 = stub.db.Column(
        stub.db.Text,
        name='forest_3',
        nullable=True,

    )
    tent_capacity = stub.db.Column(
        stub.db.Text,
        name='tent_capacity',
        nullable=True,

    )
    tour_requisites = stub.db.Column(
        stub.db.Text,
        name='tour_requisites',
        nullable=True,

    )
    anketa_status = stub.db.Column(
        stub.db.Enum(*tuple(x.value for x in enums.yasm.database.AnketaStatus)),
        name='anketa_status',
        
    )
    user_agent = stub.db.Column(
        stub.db.Text,
        name='user_agent',
        nullable=True,

    )
    fk_department_id = stub.db.Column(
        stub.db.Integer,
        name='department_id',
        
    )
    person_created = stub.db.Column(
        stub.db.Text,
        name='person_created',
        nullable=True,

    )
    person_modified = stub.db.Column(
        stub.db.Text,
        name='person_modified',
        nullable=True,

    )
    person_changedby = stub.db.Column(
        stub.db.Text,
        name='person_changedby',
        nullable=True,

    )
    other_contacts = stub.db.Column(
        stub.db.Text,
        name='other_contacts',
        nullable=True,

    )
    department = stub.db.relationship(
        'Department',
        uselist=False,
        lazy='joined',
        foreign_keys=[
            fk_department_id,
        ],
        back_populates='people',
    )
    person_schools = stub.db.relationship(
        'PersonSchool',
        uselist=True,
        lazy='select',
        back_populates='member',
    )
    exams = stub.db.relationship(
        'Exam',
        uselist=True,
        lazy='select',
        back_populates='student',
    )
    courses = stub.db.relationship(
        'CourseTeachers',
        uselist=True,
        lazy='select',
        back_populates='teacher',
    )
    comments = stub.db.relationship(
        'PersonComment',
        uselist=True,
        lazy='select',
        back_populates='blamed',
    )
    avas = stub.db.relationship(
        'Ava',
        uselist=True,
        lazy='select',
        back_populates='person',
    )
    dlogins = stub.db.relationship(
        'DirectLogin',
        uselist=True,
        lazy='select',
        back_populates='person',
    )
    contacts = stub.db.relationship(
        'Contact',
        uselist=True,
        lazy='select',
        back_populates='person',
    )
    __table_args__ = (
        stub.db.ForeignKeyConstraint(
            (
                fk_department_id,
            ),
            (
                'department.department_id',
            ),
        ),
    )
    @classmethod
    def from_json(cls, json_data):
        return cls(
            id=int(json_data['id']) if 'id' in json_data else None,
            rights=str(json_data['rights']) if 'rights' in json_data else None,
            first_name=str(json_data['first_name']) if 'first_name' in json_data else None,
            last_name=str(json_data['last_name']) if 'last_name' in json_data else None,
            patronymic=str(json_data['patronymic']) if 'patronymic' in json_data else None,
            nick_name=str(json_data['nick_name']) if 'nick_name' in json_data else None,
            birth_date=str(json_data['birth_date']) if 'birth_date' in json_data else None,
            passport_data=str(json_data['passport_data']) if 'passport_data' in json_data else None,
            school=str(json_data['school']) if 'school' in json_data else None,
            school_city=str(json_data['school_city']) if 'school_city' in json_data else None,
            ank_class=str(json_data['ank_class']) if 'ank_class' in json_data else None,
            current_class=str(json_data['current_class']) if 'current_class' in json_data else None,
            phone=str(json_data['phone']) if 'phone' in json_data else None,
            cellular=str(json_data['cellular']) if 'cellular' in json_data else None,
            email=str(json_data['email']) if 'email' in json_data else None,
            skype=str(json_data['skype']) if 'skype' in json_data else None,
            social_profile=str(json_data['social_profile']) if 'social_profile' in json_data else None,
            is_teacher=str(json_data['is_teacher']) if 'is_teacher' in json_data else None,
            is_student=str(json_data['is_student']) if 'is_student' in json_data else None,
            favourites=str(json_data['favourites']) if 'favourites' in json_data else None,
            achievements=str(json_data['achievements']) if 'achievements' in json_data else None,
            hobby=str(json_data['hobby']) if 'hobby' in json_data else None,
            lesh_ref=str(json_data['lesh_ref']) if 'lesh_ref' in json_data else None,
            forest_1=str(json_data['forest_1']) if 'forest_1' in json_data else None,
            forest_2=str(json_data['forest_2']) if 'forest_2' in json_data else None,
            forest_3=str(json_data['forest_3']) if 'forest_3' in json_data else None,
            tent_capacity=str(json_data['tent_capacity']) if 'tent_capacity' in json_data else None,
            tour_requisites=str(json_data['tour_requisites']) if 'tour_requisites' in json_data else None,
            anketa_status=enums.yasm.database.AnketaStatus(json_data['anketa_status']) if 'anketa_status' in json_data else None,
            user_agent=str(json_data['user_agent']) if 'user_agent' in json_data else None,
            department=yasm.yasm.database.Department.from_json(json_data['department']) if 'department' in json_data else None,
            person_created=str(json_data['person_created']) if 'person_created' in json_data else None,
            person_modified=str(json_data['person_modified']) if 'person_modified' in json_data else None,
            person_changedby=str(json_data['person_changedby']) if 'person_changedby' in json_data else None,
            other_contacts=str(json_data['other_contacts']) if 'other_contacts' in json_data else None,
            person_schools=[yasm.yasm.database.PersonSchool.from_json(item) for item in json_data.get('person_schools', [])],
            exams=[yasm.yasm.database.Exam.from_json(item) for item in json_data.get('exams', [])],
            courses=[yasm.yasm.database.CourseTeachers.from_json(item) for item in json_data.get('courses', [])],
            comments=[yasm.yasm.database.PersonComment.from_json(item) for item in json_data.get('comments', [])],
            avas=[yasm.yasm.database.Ava.from_json(item) for item in json_data.get('avas', [])],
            dlogins=[yasm.yasm.database.DirectLogin.from_json(item) for item in json_data.get('dlogins', [])],
            contacts=[yasm.yasm.database.Contact.from_json(item) for item in json_data.get('contacts', [])],
        )

    @classmethod
    def from_string(cls, data):
        return cls.from_json(json.loads(data))

    def to_json(self):
        self.serialized = True
        ret = dict()
        unloaded = sqlalchemy.inspect(self).unloaded

        if isinstance(self.id, int):
            ret['id'] = self.id
        if isinstance(self.rights, str):
            ret['rights'] = self.rights
        if isinstance(self.first_name, str):
            ret['first_name'] = self.first_name
        if isinstance(self.last_name, str):
            ret['last_name'] = self.last_name
        if isinstance(self.patronymic, str):
            ret['patronymic'] = self.patronymic
        if isinstance(self.nick_name, str):
            ret['nick_name'] = self.nick_name
        if isinstance(self.birth_date, str):
            ret['birth_date'] = self.birth_date
        if isinstance(self.passport_data, str):
            ret['passport_data'] = self.passport_data
        if isinstance(self.school, str):
            ret['school'] = self.school
        if isinstance(self.school_city, str):
            ret['school_city'] = self.school_city
        if isinstance(self.ank_class, str):
            ret['ank_class'] = self.ank_class
        if isinstance(self.current_class, str):
            ret['current_class'] = self.current_class
        if isinstance(self.phone, str):
            ret['phone'] = self.phone
        if isinstance(self.cellular, str):
            ret['cellular'] = self.cellular
        if isinstance(self.email, str):
            ret['email'] = self.email
        if isinstance(self.skype, str):
            ret['skype'] = self.skype
        if isinstance(self.social_profile, str):
            ret['social_profile'] = self.social_profile
        if isinstance(self.is_teacher, str):
            ret['is_teacher'] = self.is_teacher
        if isinstance(self.is_student, str):
            ret['is_student'] = self.is_student
        if isinstance(self.favourites, str):
            ret['favourites'] = self.favourites
        if isinstance(self.achievements, str):
            ret['achievements'] = self.achievements
        if isinstance(self.hobby, str):
            ret['hobby'] = self.hobby
        if isinstance(self.lesh_ref, str):
            ret['lesh_ref'] = self.lesh_ref
        if isinstance(self.forest_1, str):
            ret['forest_1'] = self.forest_1
        if isinstance(self.forest_2, str):
            ret['forest_2'] = self.forest_2
        if isinstance(self.forest_3, str):
            ret['forest_3'] = self.forest_3
        if isinstance(self.tent_capacity, str):
            ret['tent_capacity'] = self.tent_capacity
        if isinstance(self.tour_requisites, str):
            ret['tour_requisites'] = self.tour_requisites
        if isinstance(self.anketa_status, enums.yasm.database.AnketaStatus):
            ret['anketa_status'] = self.anketa_status.value
        if isinstance(self.user_agent, str):
            ret['user_agent'] = self.user_agent
        if isinstance(self.department, yasm.yasm.database.Department) and not self.department.serialized:
            ret['department'] = self.department.to_json()
        if isinstance(self.person_created, str):
            ret['person_created'] = self.person_created
        if isinstance(self.person_modified, str):
            ret['person_modified'] = self.person_modified
        if isinstance(self.person_changedby, str):
            ret['person_changedby'] = self.person_changedby
        if isinstance(self.other_contacts, str):
            ret['other_contacts'] = self.other_contacts
        if 'person_schools' not in unloaded and isinstance(self.person_schools, list):
            ret['person_schools'] = [value.to_json() for value in self.person_schools if not value.serialized]
        if 'exams' not in unloaded and isinstance(self.exams, list):
            ret['exams'] = [value.to_json() for value in self.exams if not value.serialized]
        if 'courses' not in unloaded and isinstance(self.courses, list):
            ret['courses'] = [value.to_json() for value in self.courses if not value.serialized]
        if 'comments' not in unloaded and isinstance(self.comments, list):
            ret['comments'] = [value.to_json() for value in self.comments if not value.serialized]
        if 'avas' not in unloaded and isinstance(self.avas, list):
            ret['avas'] = [value.to_json() for value in self.avas if not value.serialized]
        if 'dlogins' not in unloaded and isinstance(self.dlogins, list):
            ret['dlogins'] = [value.to_json() for value in self.dlogins if not value.serialized]
        if 'contacts' not in unloaded and isinstance(self.contacts, list):
            ret['contacts'] = [value.to_json() for value in self.contacts if not value.serialized]
        self.serialized = False
        return ret

    def to_string(self):
        return json.dumps(self.to_json())





class Department(
        stub.db.Model,    ):
    __tablename__ = 'department'

    def __init__(self, *args, **kwargs):
        self.serialized = False
        super(Department, self).__init__(*args, **kwargs)

    @sqlalchemy.orm.reconstructor
    def init_on_load(self):
        self.serialized = False

    id = stub.db.Column(
        stub.db.Integer,
        name='department_id',
        primary_key=True,
        autoincrement=True,

    )
    title = stub.db.Column(
        stub.db.Text,
        name='department_title',
        
    )
    created = stub.db.Column(
        stub.db.Text,
        name='department_created',
        
    )
    modified = stub.db.Column(
        stub.db.Text,
        name='department_modified',
        
    )
    changedby = stub.db.Column(
        stub.db.Text,
        name='department_changedby',
        
    )
    people = stub.db.relationship(
        'Person',
        uselist=True,
        lazy='select',
        back_populates='department',
    )
    person_schools = stub.db.relationship(
        'PersonSchool',
        uselist=True,
        lazy='select',
        back_populates='department',
    )
    __table_args__ = (
    )
    @classmethod
    def from_json(cls, json_data):
        return cls(
            id=int(json_data['id']) if 'id' in json_data else None,
            people=[yasm.yasm.database.Person.from_json(item) for item in json_data.get('people', [])],
            title=str(json_data['title']) if 'title' in json_data else None,
            created=str(json_data['created']) if 'created' in json_data else None,
            modified=str(json_data['modified']) if 'modified' in json_data else None,
            changedby=str(json_data['changedby']) if 'changedby' in json_data else None,
            person_schools=[yasm.yasm.database.PersonSchool.from_json(item) for item in json_data.get('person_schools', [])],
        )

    @classmethod
    def from_string(cls, data):
        return cls.from_json(json.loads(data))

    def to_json(self):
        self.serialized = True
        ret = dict()
        unloaded = sqlalchemy.inspect(self).unloaded

        if isinstance(self.id, int):
            ret['id'] = self.id
        if 'people' not in unloaded and isinstance(self.people, list):
            ret['people'] = [value.to_json() for value in self.people if not value.serialized]
        if isinstance(self.title, str):
            ret['title'] = self.title
        if isinstance(self.created, str):
            ret['created'] = self.created
        if isinstance(self.modified, str):
            ret['modified'] = self.modified
        if isinstance(self.changedby, str):
            ret['changedby'] = self.changedby
        if 'person_schools' not in unloaded and isinstance(self.person_schools, list):
            ret['person_schools'] = [value.to_json() for value in self.person_schools if not value.serialized]
        self.serialized = False
        return ret

    def to_string(self):
        return json.dumps(self.to_json())





class PersonSchool(
        stub.db.Model,    ):
    __tablename__ = 'person_school'

    def __init__(self, *args, **kwargs):
        self.serialized = False
        super(PersonSchool, self).__init__(*args, **kwargs)

    @sqlalchemy.orm.reconstructor
    def init_on_load(self):
        self.serialized = False

    id = stub.db.Column(
        stub.db.Integer,
        name='person_school_id',
        primary_key=True,
        autoincrement=True,

    )
    fk_member_id = stub.db.Column(
        stub.db.Integer,
        name='member_person_id',
        
    )
    fk_department_id = stub.db.Column(
        stub.db.Integer,
        name='member_department_id',
        
    )
    fk_school_id = stub.db.Column(
        stub.db.Integer,
        name='school_id',
        
    )
    is_student = stub.db.Column(
        stub.db.Text,
        name='is_student',
        nullable=True,

    )
    is_teacher = stub.db.Column(
        stub.db.Text,
        name='is_teacher',
        nullable=True,

    )
    curatorship = stub.db.Column(
        stub.db.Enum(*tuple(x.value for x in enums.yasm.database.Curatorship)),
        name='curatorship',
        nullable=True,

    )
    curator_group = stub.db.Column(
        stub.db.Text,
        name='curator_group',
        nullable=True,

    )
    courses_needed = stub.db.Column(
        stub.db.Text,
        name='courses_needed',
        nullable=True,

    )
    current_class = stub.db.Column(
        stub.db.Text,
        name='current_class',
        nullable=True,

    )
    comment = stub.db.Column(
        stub.db.Text,
        name='person_school_comment',
        nullable=True,

    )
    created = stub.db.Column(
        stub.db.Text,
        name='person_school_created',
        
    )
    modified = stub.db.Column(
        stub.db.Text,
        name='person_school_modified',
        
    )
    changedby = stub.db.Column(
        stub.db.Text,
        name='person_school_changedby',
        
    )
    arrival = stub.db.Column(
        stub.db.Text,
        name='frm',
        
    )
    leave = stub.db.Column(
        stub.db.Text,
        name='tll',
        
    )
    member = stub.db.relationship(
        'Person',
        uselist=False,
        lazy='joined',
        foreign_keys=[
            fk_member_id,
        ],
        back_populates='person_schools',
    )
    department = stub.db.relationship(
        'Department',
        uselist=False,
        lazy='joined',
        foreign_keys=[
            fk_department_id,
        ],
        back_populates='person_schools',
    )
    school = stub.db.relationship(
        'School',
        uselist=False,
        lazy='joined',
        foreign_keys=[
            fk_school_id,
        ],
        back_populates='person_schools',
    )
    calendars = stub.db.relationship(
        'Calendar',
        uselist=True,
        lazy='select',
        back_populates='person_school',
    )
    __table_args__ = (
        stub.db.ForeignKeyConstraint(
            (
                fk_member_id,
            ),
            (
                'person.person_id',
            ),
        ),
        stub.db.ForeignKeyConstraint(
            (
                fk_department_id,
            ),
            (
                'department.department_id',
            ),
        ),
        stub.db.ForeignKeyConstraint(
            (
                fk_school_id,
            ),
            (
                'school.school_id',
            ),
        ),
    )
    @classmethod
    def from_json(cls, json_data):
        return cls(
            id=int(json_data['id']) if 'id' in json_data else None,
            member=yasm.yasm.database.Person.from_json(json_data['member']) if 'member' in json_data else None,
            department=yasm.yasm.database.Department.from_json(json_data['department']) if 'department' in json_data else None,
            school=yasm.yasm.database.School.from_json(json_data['school']) if 'school' in json_data else None,
            is_student=str(json_data['is_student']) if 'is_student' in json_data else None,
            is_teacher=str(json_data['is_teacher']) if 'is_teacher' in json_data else None,
            curatorship=enums.yasm.database.Curatorship(json_data['curatorship']) if 'curatorship' in json_data else None,
            curator_group=str(json_data['curator_group']) if 'curator_group' in json_data else None,
            courses_needed=str(json_data['courses_needed']) if 'courses_needed' in json_data else None,
            current_class=str(json_data['current_class']) if 'current_class' in json_data else None,
            comment=str(json_data['comment']) if 'comment' in json_data else None,
            created=str(json_data['created']) if 'created' in json_data else None,
            modified=str(json_data['modified']) if 'modified' in json_data else None,
            changedby=str(json_data['changedby']) if 'changedby' in json_data else None,
            arrival=str(json_data['arrival']) if 'arrival' in json_data else None,
            leave=str(json_data['leave']) if 'leave' in json_data else None,
            calendars=[yasm.yasm.database.Calendar.from_json(item) for item in json_data.get('calendars', [])],
        )

    @classmethod
    def from_string(cls, data):
        return cls.from_json(json.loads(data))

    def to_json(self):
        self.serialized = True
        ret = dict()
        unloaded = sqlalchemy.inspect(self).unloaded

        if isinstance(self.id, int):
            ret['id'] = self.id
        if isinstance(self.member, yasm.yasm.database.Person) and not self.member.serialized:
            ret['member'] = self.member.to_json()
        if isinstance(self.department, yasm.yasm.database.Department) and not self.department.serialized:
            ret['department'] = self.department.to_json()
        if isinstance(self.school, yasm.yasm.database.School) and not self.school.serialized:
            ret['school'] = self.school.to_json()
        if isinstance(self.is_student, str):
            ret['is_student'] = self.is_student
        if isinstance(self.is_teacher, str):
            ret['is_teacher'] = self.is_teacher
        if isinstance(self.curatorship, enums.yasm.database.Curatorship):
            ret['curatorship'] = self.curatorship.value
        if isinstance(self.curator_group, str):
            ret['curator_group'] = self.curator_group
        if isinstance(self.courses_needed, str):
            ret['courses_needed'] = self.courses_needed
        if isinstance(self.current_class, str):
            ret['current_class'] = self.current_class
        if isinstance(self.comment, str):
            ret['comment'] = self.comment
        if isinstance(self.created, str):
            ret['created'] = self.created
        if isinstance(self.modified, str):
            ret['modified'] = self.modified
        if isinstance(self.changedby, str):
            ret['changedby'] = self.changedby
        if isinstance(self.arrival, str):
            ret['arrival'] = self.arrival
        if isinstance(self.leave, str):
            ret['leave'] = self.leave
        if 'calendars' not in unloaded and isinstance(self.calendars, list):
            ret['calendars'] = [value.to_json() for value in self.calendars if not value.serialized]
        self.serialized = False
        return ret

    def to_string(self):
        return json.dumps(self.to_json())





class Calendar(
        stub.db.Model,    ):
    __tablename__ = 'calendar'

    def __init__(self, *args, **kwargs):
        self.serialized = False
        super(Calendar, self).__init__(*args, **kwargs)

    @sqlalchemy.orm.reconstructor
    def init_on_load(self):
        self.serialized = False
        self.date = datetime.date(self.date)
        self.modified = datetime.datetime(self.modified)

    fk_person_school_id = stub.db.Column(
        stub.db.Integer,
        name='person_school_id',
        primary_key=True,
        
    )
    date = stub.db.Column(
        stub.db.Date,
        name='date',
        primary_key=True,
        
    )
    status = stub.db.Column(
        stub.db.Text,
        name='status',
        
    )
    modified = stub.db.Column(
        stub.db.TIMESTAMP,
        name='modified',
        
    )
    changed_by = stub.db.Column(
        stub.db.Text,
        name='changed_by',
        
    )
    person_school = stub.db.relationship(
        'PersonSchool',
        uselist=False,
        lazy='joined',
        foreign_keys=[
            fk_person_school_id,
        ],
        back_populates='calendars',
    )
    __table_args__ = (
        stub.db.ForeignKeyConstraint(
            (
                fk_person_school_id,
            ),
            (
                'person_school.person_school_id',
            ),
        ),
    )
    @classmethod
    def from_json(cls, json_data):
        return cls(
            person_school=yasm.yasm.database.PersonSchool.from_json(json_data['person_school']) if 'person_school' in json_data else None,
            date=datetime.date(json_data['date']) if 'date' in json_data else None,
            status=str(json_data['status']) if 'status' in json_data else None,
            modified=datetime.datetime(json_data['modified']) if 'modified' in json_data else None,
            changed_by=str(json_data['changed_by']) if 'changed_by' in json_data else None,
        )

    @classmethod
    def from_string(cls, data):
        return cls.from_json(json.loads(data))

    def to_json(self):
        self.serialized = True
        ret = dict()
        unloaded = sqlalchemy.inspect(self).unloaded

        if isinstance(self.person_school, yasm.yasm.database.PersonSchool) and not self.person_school.serialized:
            ret['person_school'] = self.person_school.to_json()
        if isinstance(self.date, datetime.date) and not self.date.serialized:
            ret['date'] = self.date.to_json()
        if isinstance(self.status, str):
            ret['status'] = self.status
        if isinstance(self.modified, datetime.datetime) and not self.modified.serialized:
            ret['modified'] = self.modified.to_json()
        if isinstance(self.changed_by, str):
            ret['changed_by'] = self.changed_by
        self.serialized = False
        return ret

    def to_string(self):
        return json.dumps(self.to_json())





class School(
        stub.db.Model,    ):
    __tablename__ = 'school'

    def __init__(self, *args, **kwargs):
        self.serialized = False
        super(School, self).__init__(*args, **kwargs)

    @sqlalchemy.orm.reconstructor
    def init_on_load(self):
        self.serialized = False

    id = stub.db.Column(
        stub.db.Integer,
        name='school_id',
        primary_key=True,
        autoincrement=True,

    )
    title = stub.db.Column(
        stub.db.Text,
        name='school_title',
        
    )
    type = stub.db.Column(
        stub.db.Enum(*tuple(x.value for x in enums.yasm.database.SchoolType)),
        name='school_type',
        
    )
    start = stub.db.Column(
        stub.db.Text,
        name='school_date_start',
        
    )
    end = stub.db.Column(
        stub.db.Text,
        name='school_date_end',
        
    )
    location = stub.db.Column(
        stub.db.Text,
        name='school_location',
        
    )
    coords = stub.db.Column(
        stub.db.Text,
        name='school_coords',
        
    )
    created = stub.db.Column(
        stub.db.Text,
        name='school_created',
        
    )
    modified = stub.db.Column(
        stub.db.Text,
        name='school_modified',
        
    )
    changedby = stub.db.Column(
        stub.db.Text,
        name='school_changedby',
        
    )
    person_schools = stub.db.relationship(
        'PersonSchool',
        uselist=True,
        lazy='select',
        back_populates='school',
    )
    courses = stub.db.relationship(
        'Course',
        uselist=True,
        lazy='select',
        back_populates='school',
    )
    person_comments = stub.db.relationship(
        'PersonComment',
        uselist=True,
        lazy='select',
        back_populates='school',
    )
    __table_args__ = (
    )
    @classmethod
    def from_json(cls, json_data):
        return cls(
            id=int(json_data['id']) if 'id' in json_data else None,
            title=str(json_data['title']) if 'title' in json_data else None,
            type=enums.yasm.database.SchoolType(json_data['type']) if 'type' in json_data else None,
            start=str(json_data['start']) if 'start' in json_data else None,
            end=str(json_data['end']) if 'end' in json_data else None,
            location=str(json_data['location']) if 'location' in json_data else None,
            coords=str(json_data['coords']) if 'coords' in json_data else None,
            created=str(json_data['created']) if 'created' in json_data else None,
            modified=str(json_data['modified']) if 'modified' in json_data else None,
            changedby=str(json_data['changedby']) if 'changedby' in json_data else None,
            person_schools=[yasm.yasm.database.PersonSchool.from_json(item) for item in json_data.get('person_schools', [])],
            courses=[yasm.yasm.database.Course.from_json(item) for item in json_data.get('courses', [])],
            person_comments=[yasm.yasm.database.PersonComment.from_json(item) for item in json_data.get('person_comments', [])],
        )

    @classmethod
    def from_string(cls, data):
        return cls.from_json(json.loads(data))

    def to_json(self):
        self.serialized = True
        ret = dict()
        unloaded = sqlalchemy.inspect(self).unloaded

        if isinstance(self.id, int):
            ret['id'] = self.id
        if isinstance(self.title, str):
            ret['title'] = self.title
        if isinstance(self.type, enums.yasm.database.SchoolType):
            ret['type'] = self.type.value
        if isinstance(self.start, str):
            ret['start'] = self.start
        if isinstance(self.end, str):
            ret['end'] = self.end
        if isinstance(self.location, str):
            ret['location'] = self.location
        if isinstance(self.coords, str):
            ret['coords'] = self.coords
        if isinstance(self.created, str):
            ret['created'] = self.created
        if isinstance(self.modified, str):
            ret['modified'] = self.modified
        if isinstance(self.changedby, str):
            ret['changedby'] = self.changedby
        if 'person_schools' not in unloaded and isinstance(self.person_schools, list):
            ret['person_schools'] = [value.to_json() for value in self.person_schools if not value.serialized]
        if 'courses' not in unloaded and isinstance(self.courses, list):
            ret['courses'] = [value.to_json() for value in self.courses if not value.serialized]
        if 'person_comments' not in unloaded and isinstance(self.person_comments, list):
            ret['person_comments'] = [value.to_json() for value in self.person_comments if not value.serialized]
        self.serialized = False
        return ret

    def to_string(self):
        return json.dumps(self.to_json())





class Course(
        stub.db.Model,    ):
    __tablename__ = 'course'

    def __init__(self, *args, **kwargs):
        self.serialized = False
        super(Course, self).__init__(*args, **kwargs)

    @sqlalchemy.orm.reconstructor
    def init_on_load(self):
        self.serialized = False

    id = stub.db.Column(
        stub.db.Integer,
        name='course_id',
        primary_key=True,
        autoincrement=True,

    )
    title = stub.db.Column(
        stub.db.Text,
        name='course_title',
        
    )
    fk_school_id = stub.db.Column(
        stub.db.Integer,
        name='school_id',
        
    )
    cycle = stub.db.Column(
        stub.db.Text,
        name='course_cycle',
        
    )
    target_class = stub.db.Column(
        stub.db.Text,
        name='target_class',
        
    )
    desc = stub.db.Column(
        stub.db.Text,
        name='course_desc',
        
    )
    type = stub.db.Column(
        stub.db.Enum(*tuple(x.value for x in enums.yasm.database.CourseType)),
        name='course_type',
        
    )
    area = stub.db.Column(
        stub.db.Enum(*tuple(x.value for x in enums.yasm.database.CourseArea)),
        name='course_area',
        
    )
    created = stub.db.Column(
        stub.db.Text,
        name='course_created',
        
    )
    modified = stub.db.Column(
        stub.db.Text,
        name='course_modified',
        
    )
    changedby = stub.db.Column(
        stub.db.Text,
        name='course_changedby',
        
    )
    school = stub.db.relationship(
        'School',
        uselist=False,
        lazy='joined',
        foreign_keys=[
            fk_school_id,
        ],
        back_populates='courses',
    )
    teachers = stub.db.relationship(
        'CourseTeachers',
        uselist=True,
        lazy='select',
        back_populates='course',
    )
    exams = stub.db.relationship(
        'Exam',
        uselist=True,
        lazy='select',
        back_populates='course',
    )
    __table_args__ = (
        stub.db.ForeignKeyConstraint(
            (
                fk_school_id,
            ),
            (
                'school.school_id',
            ),
        ),
    )
    @classmethod
    def from_json(cls, json_data):
        return cls(
            id=int(json_data['id']) if 'id' in json_data else None,
            title=str(json_data['title']) if 'title' in json_data else None,
            school=yasm.yasm.database.School.from_json(json_data['school']) if 'school' in json_data else None,
            cycle=str(json_data['cycle']) if 'cycle' in json_data else None,
            target_class=str(json_data['target_class']) if 'target_class' in json_data else None,
            desc=str(json_data['desc']) if 'desc' in json_data else None,
            type=enums.yasm.database.CourseType(json_data['type']) if 'type' in json_data else None,
            area=enums.yasm.database.CourseArea(json_data['area']) if 'area' in json_data else None,
            created=str(json_data['created']) if 'created' in json_data else None,
            modified=str(json_data['modified']) if 'modified' in json_data else None,
            changedby=str(json_data['changedby']) if 'changedby' in json_data else None,
            teachers=[yasm.yasm.database.CourseTeachers.from_json(item) for item in json_data.get('teachers', [])],
            exams=[yasm.yasm.database.Exam.from_json(item) for item in json_data.get('exams', [])],
        )

    @classmethod
    def from_string(cls, data):
        return cls.from_json(json.loads(data))

    def to_json(self):
        self.serialized = True
        ret = dict()
        unloaded = sqlalchemy.inspect(self).unloaded

        if isinstance(self.id, int):
            ret['id'] = self.id
        if isinstance(self.title, str):
            ret['title'] = self.title
        if isinstance(self.school, yasm.yasm.database.School) and not self.school.serialized:
            ret['school'] = self.school.to_json()
        if isinstance(self.cycle, str):
            ret['cycle'] = self.cycle
        if isinstance(self.target_class, str):
            ret['target_class'] = self.target_class
        if isinstance(self.desc, str):
            ret['desc'] = self.desc
        if isinstance(self.type, enums.yasm.database.CourseType):
            ret['type'] = self.type.value
        if isinstance(self.area, enums.yasm.database.CourseArea):
            ret['area'] = self.area.value
        if isinstance(self.created, str):
            ret['created'] = self.created
        if isinstance(self.modified, str):
            ret['modified'] = self.modified
        if isinstance(self.changedby, str):
            ret['changedby'] = self.changedby
        if 'teachers' not in unloaded and isinstance(self.teachers, list):
            ret['teachers'] = [value.to_json() for value in self.teachers if not value.serialized]
        if 'exams' not in unloaded and isinstance(self.exams, list):
            ret['exams'] = [value.to_json() for value in self.exams if not value.serialized]
        self.serialized = False
        return ret

    def to_string(self):
        return json.dumps(self.to_json())





class CourseTeachers(
        stub.db.Model,    ):
    __tablename__ = 'course_teachers'

    def __init__(self, *args, **kwargs):
        self.serialized = False
        super(CourseTeachers, self).__init__(*args, **kwargs)

    @sqlalchemy.orm.reconstructor
    def init_on_load(self):
        self.serialized = False

    id = stub.db.Column(
        stub.db.Integer,
        name='course_teachers_id',
        primary_key=True,
        autoincrement=True,

    )
    fk_course_id = stub.db.Column(
        stub.db.Integer,
        name='course_id',
        
    )
    fk_teacher_id = stub.db.Column(
        stub.db.Integer,
        name='course_teacher_id',
        
    )
    created = stub.db.Column(
        stub.db.Text,
        name='course_teachers_created',
        
    )
    modified = stub.db.Column(
        stub.db.Text,
        name='course_teachers_modified',
        
    )
    changedby = stub.db.Column(
        stub.db.Text,
        name='course_teachers_changedby',
        
    )
    course = stub.db.relationship(
        'Course',
        uselist=False,
        lazy='joined',
        foreign_keys=[
            fk_course_id,
        ],
        back_populates='teachers',
    )
    teacher = stub.db.relationship(
        'Person',
        uselist=False,
        lazy='joined',
        foreign_keys=[
            fk_teacher_id,
        ],
        back_populates='courses',
    )
    __table_args__ = (
        stub.db.ForeignKeyConstraint(
            (
                fk_course_id,
            ),
            (
                'course.course_id',
            ),
        ),
        stub.db.ForeignKeyConstraint(
            (
                fk_teacher_id,
            ),
            (
                'person.person_id',
            ),
        ),
    )
    @classmethod
    def from_json(cls, json_data):
        return cls(
            id=int(json_data['id']) if 'id' in json_data else None,
            course=yasm.yasm.database.Course.from_json(json_data['course']) if 'course' in json_data else None,
            teacher=yasm.yasm.database.Person.from_json(json_data['teacher']) if 'teacher' in json_data else None,
            created=str(json_data['created']) if 'created' in json_data else None,
            modified=str(json_data['modified']) if 'modified' in json_data else None,
            changedby=str(json_data['changedby']) if 'changedby' in json_data else None,
        )

    @classmethod
    def from_string(cls, data):
        return cls.from_json(json.loads(data))

    def to_json(self):
        self.serialized = True
        ret = dict()
        unloaded = sqlalchemy.inspect(self).unloaded

        if isinstance(self.id, int):
            ret['id'] = self.id
        if isinstance(self.course, yasm.yasm.database.Course) and not self.course.serialized:
            ret['course'] = self.course.to_json()
        if isinstance(self.teacher, yasm.yasm.database.Person) and not self.teacher.serialized:
            ret['teacher'] = self.teacher.to_json()
        if isinstance(self.created, str):
            ret['created'] = self.created
        if isinstance(self.modified, str):
            ret['modified'] = self.modified
        if isinstance(self.changedby, str):
            ret['changedby'] = self.changedby
        self.serialized = False
        return ret

    def to_string(self):
        return json.dumps(self.to_json())





class Exam(
        stub.db.Model,    ):
    __tablename__ = 'exam'

    def __init__(self, *args, **kwargs):
        self.serialized = False
        super(Exam, self).__init__(*args, **kwargs)

    @sqlalchemy.orm.reconstructor
    def init_on_load(self):
        self.serialized = False

    id = stub.db.Column(
        stub.db.Integer,
        name='exam_id',
        primary_key=True,
        autoincrement=True,

    )
    fk_student_id = stub.db.Column(
        stub.db.Integer,
        name='student_person_id',
        
    )
    fk_course_id = stub.db.Column(
        stub.db.Integer,
        name='course_id',
        
    )
    status = stub.db.Column(
        stub.db.Text,
        name='exam_status',
        nullable=True,

    )
    deadline_date = stub.db.Column(
        stub.db.Text,
        name='deadline_date',
        nullable=True,

    )
    comment = stub.db.Column(
        stub.db.Text,
        name='exam_comment',
        nullable=True,

    )
    created = stub.db.Column(
        stub.db.Text,
        name='exam_created',
        
    )
    modified = stub.db.Column(
        stub.db.Text,
        name='exam_modified',
        
    )
    changedby = stub.db.Column(
        stub.db.Text,
        name='exam_changedby',
        
    )
    student = stub.db.relationship(
        'Person',
        uselist=False,
        lazy='joined',
        foreign_keys=[
            fk_student_id,
        ],
        back_populates='exams',
    )
    course = stub.db.relationship(
        'Course',
        uselist=False,
        lazy='joined',
        foreign_keys=[
            fk_course_id,
        ],
        back_populates='exams',
    )
    __table_args__ = (
        stub.db.ForeignKeyConstraint(
            (
                fk_student_id,
            ),
            (
                'person.person_id',
            ),
        ),
        stub.db.ForeignKeyConstraint(
            (
                fk_course_id,
            ),
            (
                'course.course_id',
            ),
        ),
    )
    @classmethod
    def from_json(cls, json_data):
        return cls(
            id=int(json_data['id']) if 'id' in json_data else None,
            student=yasm.yasm.database.Person.from_json(json_data['student']) if 'student' in json_data else None,
            course=yasm.yasm.database.Course.from_json(json_data['course']) if 'course' in json_data else None,
            status=str(json_data['status']) if 'status' in json_data else None,
            deadline_date=str(json_data['deadline_date']) if 'deadline_date' in json_data else None,
            comment=str(json_data['comment']) if 'comment' in json_data else None,
            created=str(json_data['created']) if 'created' in json_data else None,
            modified=str(json_data['modified']) if 'modified' in json_data else None,
            changedby=str(json_data['changedby']) if 'changedby' in json_data else None,
        )

    @classmethod
    def from_string(cls, data):
        return cls.from_json(json.loads(data))

    def to_json(self):
        self.serialized = True
        ret = dict()
        unloaded = sqlalchemy.inspect(self).unloaded

        if isinstance(self.id, int):
            ret['id'] = self.id
        if isinstance(self.student, yasm.yasm.database.Person) and not self.student.serialized:
            ret['student'] = self.student.to_json()
        if isinstance(self.course, yasm.yasm.database.Course) and not self.course.serialized:
            ret['course'] = self.course.to_json()
        if isinstance(self.status, str):
            ret['status'] = self.status
        if isinstance(self.deadline_date, str):
            ret['deadline_date'] = self.deadline_date
        if isinstance(self.comment, str):
            ret['comment'] = self.comment
        if isinstance(self.created, str):
            ret['created'] = self.created
        if isinstance(self.modified, str):
            ret['modified'] = self.modified
        if isinstance(self.changedby, str):
            ret['changedby'] = self.changedby
        self.serialized = False
        return ret

    def to_string(self):
        return json.dumps(self.to_json())





class PersonComment(
        stub.db.Model,    ):
    __tablename__ = 'person_comment'

    def __init__(self, *args, **kwargs):
        self.serialized = False
        super(PersonComment, self).__init__(*args, **kwargs)

    @sqlalchemy.orm.reconstructor
    def init_on_load(self):
        self.serialized = False

    id = stub.db.Column(
        stub.db.Integer,
        name='person_comment_id',
        primary_key=True,
        autoincrement=True,

    )
    fk_blamed_id = stub.db.Column(
        stub.db.Integer,
        name='blamed_person_id',
        
    )
    fk_school_id = stub.db.Column(
        stub.db.Integer,
        name='school_id',
        
    )
    owner_login = stub.db.Column(
        stub.db.Text,
        name='owner_login',
        
    )
    record_acl = stub.db.Column(
        stub.db.Text,
        name='record_acl',
        nullable=True,

    )
    deleted = stub.db.Column(
        stub.db.Text,
        name='person_comment_deleted',
        nullable=True,

    )
    created = stub.db.Column(
        stub.db.Text,
        name='person_comment_created',
        
    )
    modified = stub.db.Column(
        stub.db.Text,
        name='person_comment_modified',
        
    )
    changedby = stub.db.Column(
        stub.db.Text,
        name='person_comment_changedby',
        
    )
    blamed = stub.db.relationship(
        'Person',
        uselist=False,
        lazy='joined',
        foreign_keys=[
            fk_blamed_id,
        ],
        back_populates='comments',
    )
    school = stub.db.relationship(
        'School',
        uselist=False,
        lazy='joined',
        foreign_keys=[
            fk_school_id,
        ],
        back_populates='person_comments',
    )
    __table_args__ = (
        stub.db.ForeignKeyConstraint(
            (
                fk_blamed_id,
            ),
            (
                'person.person_id',
            ),
        ),
        stub.db.ForeignKeyConstraint(
            (
                fk_school_id,
            ),
            (
                'school.school_id',
            ),
        ),
    )
    @classmethod
    def from_json(cls, json_data):
        return cls(
            id=int(json_data['id']) if 'id' in json_data else None,
            blamed=yasm.yasm.database.Person.from_json(json_data['blamed']) if 'blamed' in json_data else None,
            school=yasm.yasm.database.School.from_json(json_data['school']) if 'school' in json_data else None,
            owner_login=str(json_data['owner_login']) if 'owner_login' in json_data else None,
            record_acl=str(json_data['record_acl']) if 'record_acl' in json_data else None,
            deleted=str(json_data['deleted']) if 'deleted' in json_data else None,
            created=str(json_data['created']) if 'created' in json_data else None,
            modified=str(json_data['modified']) if 'modified' in json_data else None,
            changedby=str(json_data['changedby']) if 'changedby' in json_data else None,
        )

    @classmethod
    def from_string(cls, data):
        return cls.from_json(json.loads(data))

    def to_json(self):
        self.serialized = True
        ret = dict()
        unloaded = sqlalchemy.inspect(self).unloaded

        if isinstance(self.id, int):
            ret['id'] = self.id
        if isinstance(self.blamed, yasm.yasm.database.Person) and not self.blamed.serialized:
            ret['blamed'] = self.blamed.to_json()
        if isinstance(self.school, yasm.yasm.database.School) and not self.school.serialized:
            ret['school'] = self.school.to_json()
        if isinstance(self.owner_login, str):
            ret['owner_login'] = self.owner_login
        if isinstance(self.record_acl, str):
            ret['record_acl'] = self.record_acl
        if isinstance(self.deleted, str):
            ret['deleted'] = self.deleted
        if isinstance(self.created, str):
            ret['created'] = self.created
        if isinstance(self.modified, str):
            ret['modified'] = self.modified
        if isinstance(self.changedby, str):
            ret['changedby'] = self.changedby
        self.serialized = False
        return ret

    def to_string(self):
        return json.dumps(self.to_json())





class Ava(
        stub.db.Model,    ):
    __tablename__ = 'ava'

    def __init__(self, *args, **kwargs):
        self.serialized = False
        super(Ava, self).__init__(*args, **kwargs)

    @sqlalchemy.orm.reconstructor
    def init_on_load(self):
        self.serialized = False

    id = stub.db.Column(
        stub.db.Integer,
        name='id',
        primary_key=True,
        autoincrement=True,

    )
    fk_person_id = stub.db.Column(
        stub.db.Integer,
        name='person_id',
        
    )
    ava = stub.db.Column(
        stub.db.Text,
        name='ava',
        
    )
    person = stub.db.relationship(
        'Person',
        uselist=False,
        lazy='joined',
        foreign_keys=[
            fk_person_id,
        ],
        back_populates='avas',
    )
    __table_args__ = (
        stub.db.ForeignKeyConstraint(
            (
                fk_person_id,
            ),
            (
                'person.person_id',
            ),
        ),
    )
    @classmethod
    def from_json(cls, json_data):
        return cls(
            id=int(json_data['id']) if 'id' in json_data else None,
            person=yasm.yasm.database.Person.from_json(json_data['person']) if 'person' in json_data else None,
            ava=str(json_data['ava']) if 'ava' in json_data else None,
        )

    @classmethod
    def from_string(cls, data):
        return cls.from_json(json.loads(data))

    def to_json(self):
        self.serialized = True
        ret = dict()
        unloaded = sqlalchemy.inspect(self).unloaded

        if isinstance(self.id, int):
            ret['id'] = self.id
        if isinstance(self.person, yasm.yasm.database.Person) and not self.person.serialized:
            ret['person'] = self.person.to_json()
        if isinstance(self.ava, str):
            ret['ava'] = self.ava
        self.serialized = False
        return ret

    def to_string(self):
        return json.dumps(self.to_json())





class DirectLogin(
        stub.db.Model,    ):
    __tablename__ = 'direct_login'

    def __init__(self, *args, **kwargs):
        self.serialized = False
        super(DirectLogin, self).__init__(*args, **kwargs)

    @sqlalchemy.orm.reconstructor
    def init_on_load(self):
        self.serialized = False

    type = stub.db.Column(
        stub.db.Text,
        name='person_comment_id',
        primary_key=True,
        
    )
    fk_person_id = stub.db.Column(
        stub.db.Integer,
        name='person_id',
        primary_key=True,
        
    )
    password_hash = stub.db.Column(
        stub.db.Text,
        name='password_hash',
        
    )
    login = stub.db.Column(
        stub.db.Text,
        name='login',
        
    )
    person = stub.db.relationship(
        'Person',
        uselist=False,
        lazy='joined',
        foreign_keys=[
            fk_person_id,
        ],
        back_populates='dlogins',
    )
    __table_args__ = (
        stub.db.ForeignKeyConstraint(
            (
                fk_person_id,
            ),
            (
                'person.person_id',
            ),
        ),
    )
    @classmethod
    def from_json(cls, json_data):
        return cls(
            type=str(json_data['type']) if 'type' in json_data else None,
            person=yasm.yasm.database.Person.from_json(json_data['person']) if 'person' in json_data else None,
            password_hash=str(json_data['password_hash']) if 'password_hash' in json_data else None,
            login=str(json_data['login']) if 'login' in json_data else None,
        )

    @classmethod
    def from_string(cls, data):
        return cls.from_json(json.loads(data))

    def to_json(self):
        self.serialized = True
        ret = dict()
        unloaded = sqlalchemy.inspect(self).unloaded

        if isinstance(self.type, str):
            ret['type'] = self.type
        if isinstance(self.person, yasm.yasm.database.Person) and not self.person.serialized:
            ret['person'] = self.person.to_json()
        if isinstance(self.password_hash, str):
            ret['password_hash'] = self.password_hash
        if isinstance(self.login, str):
            ret['login'] = self.login
        self.serialized = False
        return ret

    def to_string(self):
        return json.dumps(self.to_json())





class Contact(
        stub.db.Model,    ):
    __tablename__ = 'contact'

    def __init__(self, *args, **kwargs):
        self.serialized = False
        super(Contact, self).__init__(*args, **kwargs)

    @sqlalchemy.orm.reconstructor
    def init_on_load(self):
        self.serialized = False

    id = stub.db.Column(
        stub.db.Integer,
        name='person_comment_id',
        primary_key=True,
        autoincrement=True,

    )
    fk_person_id = stub.db.Column(
        stub.db.Integer,
        name='person_id',
        
    )
    name = stub.db.Column(
        stub.db.Text,
        name='name',
        
    )
    value = stub.db.Column(
        stub.db.Text,
        name='value',
        
    )
    person = stub.db.relationship(
        'Person',
        uselist=False,
        lazy='joined',
        foreign_keys=[
            fk_person_id,
        ],
        back_populates='contacts',
    )
    __table_args__ = (
        stub.db.ForeignKeyConstraint(
            (
                fk_person_id,
            ),
            (
                'person.person_id',
            ),
        ),
    )
    @classmethod
    def from_json(cls, json_data):
        return cls(
            id=int(json_data['id']) if 'id' in json_data else None,
            person=yasm.yasm.database.Person.from_json(json_data['person']) if 'person' in json_data else None,
            name=str(json_data['name']) if 'name' in json_data else None,
            value=str(json_data['value']) if 'value' in json_data else None,
        )

    @classmethod
    def from_string(cls, data):
        return cls.from_json(json.loads(data))

    def to_json(self):
        self.serialized = True
        ret = dict()
        unloaded = sqlalchemy.inspect(self).unloaded

        if isinstance(self.id, int):
            ret['id'] = self.id
        if isinstance(self.person, yasm.yasm.database.Person) and not self.person.serialized:
            ret['person'] = self.person.to_json()
        if isinstance(self.name, str):
            ret['name'] = self.name
        if isinstance(self.value, str):
            ret['value'] = self.value
        self.serialized = False
        return ret

    def to_string(self):
        return json.dumps(self.to_json())




