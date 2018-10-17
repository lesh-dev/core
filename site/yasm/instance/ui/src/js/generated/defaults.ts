import {Notification, NotificationList, Department, DepartmentList, Person, PersonList, Contact, ContactList, School, SchoolList, Course, CourseList, CourseTeachers, CourseTeachersList, Exam, ExamList, PersonSchool, PersonSchoolList, PersonComment, PersonCommentList, Submission, SubmissionList, Contestants, ContestantsList, Problems, ProblemsList, Solutions, SolutionsList, } from "./interfaces"

export const default_Notification = {
    notification_id: 0,
    mail_group: "mail_group",
    notification_text: "notification_text",
    notification_html: "notification_html",
} as Notification;

export const default_Department = {
    department_id: 0,
    department_title: "department_title",
    department_created: "department_created",
    department_modified: "department_modified",
    department_changedby: "department_changedby",
    person_list: {values: [], length: 0} as PersonList,
    person_school_list: {values: [], length: 0} as PersonSchoolList,
} as Department;

export const default_Person = {
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
    contact_list: {values: [], length: 0} as ContactList,
    course_teachers_list: {values: [], length: 0} as CourseTeachersList,
    exam_list: {values: [], length: 0} as ExamList,
    person_school_list: {values: [], length: 0} as PersonSchoolList,
    person_comment_list: {values: [], length: 0} as PersonCommentList,
} as Person;

export const default_Contact = {
    id: 0,
    person_id: 0,
    person: default_Person,
    name: "name",
    value: "value",
} as Contact;

export const default_School = {
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
    course_list: {values: [], length: 0} as CourseList,
    person_school_list: {values: [], length: 0} as PersonSchoolList,
    person_comment_list: {values: [], length: 0} as PersonCommentList,
} as School;

export const default_Course = {
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
    course_teachers_list: {values: [], length: 0} as CourseTeachersList,
    exam_list: {values: [], length: 0} as ExamList,
} as Course;

export const default_CourseTeachers = {
    course_teachers_id: 0,
    course_id: 0,
    course: default_Course,
    course_teacher_id: 0,
    course_teacher: default_Person,
    course_teachers_created: "course_teachers_created",
    course_teachers_modified: "course_teachers_modified",
    course_teachers_changedby: "course_teachers_changedby",
} as CourseTeachers;

export const default_Exam = {
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
} as Exam;

export const default_PersonSchool = {
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
} as PersonSchool;

export const default_PersonComment = {
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
} as PersonComment;

export const default_Submission = {
    submission_id: 0,
    mail: "mail",
    attachment: "attachment",
    fileexchange: "fileexchange",
    submission_timestamp: "submission_timestamp",
    sender: "sender",
    replied: "replied",
    processed: "processed",
    contest_year: "contest_year",
} as Submission;

export const default_Contestants = {
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
    solutions_list: {values: [], length: 0} as SolutionsList,
} as Contestants;

export const default_Problems = {
    problems_id: 0,
    contest_year: "contest_year",
    problem_name: "problem_name",
    problem_html: "problem_html",
    people: "people",
    criteria: "criteria",
    solutions_list: {values: [], length: 0} as SolutionsList,
} as Problems;

export const default_Solutions = {
    solutions_id: 0,
    problem_id: 0,
    problem: default_Problems,
    contest_year: "contest_year",
    contestant_id: 0,
    contestant: default_Contestants,
    resolution_text: "resolution_text",
    resolution_author: "resolution_author",
    resolution_mark: "resolution_mark",
} as Solutions;

