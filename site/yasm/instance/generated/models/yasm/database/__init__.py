import json
import sqlalchemy
from ... import stub
from ... import yasm
from .... import enums



@stub.add_search
class Person(stub.db.Model):
    __tablename__ = 'person'

    def __init__(self, *args, **kwargs):
        self.serialized = False
        super(Person, self).__init__(*args, **kwargs)

    @sqlalchemy.orm.reconstructor
    def init_on_load(self):
        self.serialized = False

    id = stub.db.Column(
        stub.db.Integer,
        name='person_id',
        primary_key=True,
        
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
        stub.db.Enum(enums.yasm.database.AnketaStatus),
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
        self.serialized = False
        return ret

    def to_string(self):
        return json.dumps(self.to_json())





class Department(stub.db.Model):
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
        
    )
    people = stub.db.relationship(
        'Person',
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
        self.serialized = False
        return ret

    def to_string(self):
        return json.dumps(self.to_json())




