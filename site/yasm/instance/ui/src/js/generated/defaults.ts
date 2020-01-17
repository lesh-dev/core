import {Notification, Department, Person, Ava, DirectLogin, Contact, School, Course, CourseTeachers, Exam, PersonSchool, Calendar, PersonComment, Submission, Contestants, Problems, Solutions, } from "./interfaces"

export var default_Notification: Notification;
export var default_Department: Department;
export var default_Person: Person;
export var default_Ava: Ava;
export var default_DirectLogin: DirectLogin;
export var default_Contact: Contact;
export var default_School: School;
export var default_Course: Course;
export var default_CourseTeachers: CourseTeachers;
export var default_Exam: Exam;
export var default_PersonSchool: PersonSchool;
export var default_Calendar: Calendar;
export var default_PersonComment: PersonComment;
export var default_Submission: Submission;
export var default_Contestants: Contestants;
export var default_Problems: Problems;
export var default_Solutions: Solutions;


default_Notification = {
    notification_id: 0,
    mail_group: "mail_group",
    notification_text: "notification_text",
    notification_html: "notification_html",
};

default_Department = {
    department_id: 0,
    department_title: "department_title",
    department_created: "department_created",
    department_modified: "department_modified",
    department_changedby: "department_changedby",
    persons: [] as Person[],
    person_schools: [] as PersonSchool[],
};

default_Person = {
    person_id: 0,
    rights: "rights",
    last_name: "last_name",
    first_name: "first_name",
    patronymic: "patronymic",
    nick_name: "nick_name",
    birth_date: "birth_date",
    passport_data: "passport_data",
    school: "school",
    school_city: "school_city",
    ank_class: "ank_class",
    current_class: "current_class",
    phone: "phone",
    cellular: "cellular",
    email: "email",
    skype: "skype",
    social_profile: "social_profile",
    is_teacher: "is_teacher",
    is_student: "is_student",
    favourites: "favourites",
    achievements: "achievements",
    hobby: "hobby",
    lesh_ref: "lesh_ref",
    forest_1: "forest_1",
    forest_2: "forest_2",
    forest_3: "forest_3",
    tent_capacity: "tent_capacity",
    tour_requisites: "tour_requisites",
    anketa_status: "anketa_status",
    user_agent: "user_agent",
    department_id: 0,
    department: default_Department,
    person_created: "person_created",
    person_modified: "person_modified",
    person_changedby: "person_changedby",
    other_contacts: "other_contacts",
    avas: [] as Ava[],
    direct_login: [] as DirectLogin[],
    contacts: [] as Contact[],
    course_teachers: [] as CourseTeachers[],
    exams: [] as Exam[],
    person_schools: [] as PersonSchool[],
    person_comments: [] as PersonComment[],
};

default_Ava = {
    id: 0,
    person_id: 0,
    person: default_Person,
    ava: "ava",
    entry_state: "entry_state",
};

default_DirectLogin = {
    type: "type",
    person_id: 0,
    person: default_Person,
    login: "login",
    password_hash: "password_hash",
};

default_Contact = {
    id: 0,
    person_id: 0,
    person: default_Person,
    name: "name",
    value: "value",
};

default_School = {
    school_id: 0,
    school_title: "school_title",
    school_type: "school_type",
    school_date_start: "school_date_start",
    school_date_end: "school_date_end",
    school_location: "school_location",
    school_coords: "school_coords",
    school_created: "school_created",
    school_modified: "school_modified",
    school_changedby: "school_changedby",
    courses: [] as Course[],
    person_schools: [] as PersonSchool[],
    person_comments: [] as PersonComment[],
};

default_Course = {
    course_id: 0,
    course_title: "course_title",
    school_id: 0,
    school: default_School,
    course_cycle: "course_cycle",
    target_class: "target_class",
    course_desc: "course_desc",
    course_type: "course_type",
    course_area: "course_area",
    course_comment: "course_comment",
    course_created: "course_created",
    course_modified: "course_modified",
    course_changedby: "course_changedby",
    course_teachers: [] as CourseTeachers[],
    exams: [] as Exam[],
};

default_CourseTeachers = {
    course_teachers_id: 0,
    course_id: 0,
    course: default_Course,
    course_teacher_id: 0,
    course_teacher: default_Person,
    course_teachers_created: "course_teachers_created",
    course_teachers_modified: "course_teachers_modified",
    course_teachers_changedby: "course_teachers_changedby",
};

default_Exam = {
    exam_id: 0,
    student_person_id: 0,
    student: default_Person,
    course_id: 0,
    course: default_Course,
    exam_status: "exam_status",
    deadline_date: "deadline_date",
    exam_comment: "exam_comment",
    exam_created: "exam_created",
    exam_modified: "exam_modified",
    exam_changedby: "exam_changedby",
};

default_PersonSchool = {
    person_school_id: 0,
    member_person_id: 0,
    member_person: default_Person,
    member_department_id: 0,
    department: default_Department,
    school_id: 0,
    school: default_School,
    is_student: "is_student",
    is_teacher: "is_teacher",
    curatorship: "curatorship",
    curator_group: "curator_group",
    current_class: "current_class",
    courses_needed: "courses_needed",
    person_school_comment: "person_school_comment",
    person_school_created: "person_school_created",
    person_school_modified: "person_school_modified",
    person_school_changedby: "person_school_changedby",
    frm: "frm",
    tll: "tll",
    calendars: [] as Calendar[],
};

default_Calendar = {
    person_school_id: 0,
    person_school: default_PersonSchool,
    date: new Date(),
    status: "status",
    calendar_modified: 0,
    changed_by: "changed_by",
};

default_PersonComment = {
    person_comment_id: 0,
    comment_text: "comment_text",
    blamed_person_id: 0,
    blamed_person: default_Person,
    school_id: 0,
    school: default_School,
    owner_login: "owner_login",
    record_acl: "record_acl",
    person_comment_created: "person_comment_created",
    person_comment_modified: "person_comment_modified",
    person_comment_deleted: "person_comment_deleted",
    person_comment_changedby: "person_comment_changedby",
};

default_Submission = {
    submission_id: 0,
    mail: "mail",
    attachment: "attachment",
    fileexchange: "fileexchange",
    submission_timestamp: "submission_timestamp",
    sender: "sender",
    replied: "replied",
    processed: "processed",
    contest_year: "contest_year",
};

default_Contestants = {
    contestants_id: 0,
    name: "name",
    mail: "mail",
    phone: "phone",
    parents: "parents",
    address: "address",
    school: "school",
    level: "level",
    teacher_name: "teacher_name",
    work: "work",
    fileexchange: "fileexchange",
    status: "status",
    contest_year: "contest_year",
    solutions: [] as Solutions[],
};

default_Problems = {
    problems_id: 0,
    contest_year: "contest_year",
    problem_name: "problem_name",
    problem_html: "problem_html",
    people: "people",
    criteria: "criteria",
    solutions: [] as Solutions[],
};

default_Solutions = {
    solutions_id: 0,
    problem_id: 0,
    problem: default_Problems,
    contest_year: "contest_year",
    contestant_id: 0,
    contestant: default_Contestants,
    resolution_text: "resolution_text",
    resolution_author: "resolution_author",
    resolution_mark: "resolution_mark",
};

