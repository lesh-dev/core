export interface Users {
    id: number,
    social_id: string,
    nickname: string,
    email: string,
}

export interface UsersList {
    values: Users[],
    length: number
}

export interface Notification {
    notification_id: number,
    mail_group: string,
    notification_text: string,
    notification_html: string,
}

export interface NotificationList {
    values: Notification[],
    length: number
}

export interface Department {
    department_id: number,
    department_title: string,
    department_created: string,
    department_modified: string,
    department_changedby: string,
    person_list: PersonList,
    person_school_list: PersonSchoolList,
}

export interface DepartmentList {
    values: Department[],
    length: number
}

export interface Person {
    person_id: number,
    last_name: string,
    first_name: string,
    patronymic: string,
    nick_name: string,
    birth_date: string,
    passport_data: string,
    school: string,
    school_city: string,
    ank_class: string,
    current_class: string,
    phone: string,
    cellular: string,
    email: string,
    skype: string,
    social_profile: string,
    is_teacher: string,
    is_student: string,
    favourites: string,
    achievements: string,
    hobby: string,
    lesh_ref: string,
    forest_1: string,
    forest_2: string,
    forest_3: string,
    tent_capacity: string,
    tour_requisites: string,
    anketa_status: string,
    user_agent: string,
    department_id: number,
    department_id_fk: Department,
    person_created: string,
    person_modified: string,
    person_changedby: string,
    contact_list: ContactList,
    course_teachers_list: CourseTeachersList,
    exam_list: ExamList,
    person_school_list: PersonSchoolList,
    person_comment_list: PersonCommentList,
}

export interface PersonList {
    values: Person[],
    length: number
}

export interface Contact {
    id: number,
    person_id: number,
    person_id_fk: Person,
    name: string,
    value: string,
}

export interface ContactList {
    values: Contact[],
    length: number
}

export interface School {
    school_id: number,
    school_title: string,
    school_type: string,
    school_date_start: string,
    school_date_end: string,
    school_location: string,
    school_coords: string,
    school_created: string,
    school_modified: string,
    school_changedby: string,
    course_list: CourseList,
    person_school_list: PersonSchoolList,
    person_comment_list: PersonCommentList,
}

export interface SchoolList {
    values: School[],
    length: number
}

export interface Course {
    course_id: number,
    course_title: string,
    school_id: number,
    school_id_fk: School,
    course_cycle: string,
    target_class: string,
    course_desc: string,
    course_type: string,
    course_area: string,
    course_comment: string,
    course_created: string,
    course_modified: string,
    course_changedby: string,
    course_teachers_list: CourseTeachersList,
    exam_list: ExamList,
}

export interface CourseList {
    values: Course[],
    length: number
}

export interface CourseTeachers {
    course_teachers_id: number,
    course_id: number,
    course_id_fk: Course,
    course_teacher_id: number,
    course_teacher_id_fk: Person,
    course_teachers_created: string,
    course_teachers_modified: string,
    course_teachers_changedby: string,
}

export interface CourseTeachersList {
    values: CourseTeachers[],
    length: number
}

export interface Exam {
    exam_id: number,
    student_person_id: number,
    student_person_id_fk: Person,
    course_id: number,
    course_id_fk: Course,
    exam_status: string,
    deadline_date: string,
    exam_comment: string,
    exam_created: string,
    exam_modified: string,
    exam_changedby: string,
}

export interface ExamList {
    values: Exam[],
    length: number
}

export interface PersonSchool {
    person_school_id: number,
    member_person_id: number,
    member_person_id_fk: Person,
    member_department_id: number,
    member_department_id_fk: Department,
    school_id: number,
    school_id_fk: School,
    is_student: string,
    is_teacher: string,
    curatorship: string,
    curator_group: string,
    current_class: string,
    courses_needed: string,
    person_school_comment: string,
    person_school_created: string,
    person_school_modified: string,
    person_school_changedby: string,
    frm: string,
    tll: string,
}

export interface PersonSchoolList {
    values: PersonSchool[],
    length: number
}

export interface PersonComment {
    person_comment_id: number,
    comment_text: string,
    blamed_person_id: number,
    blamed_person_id_fk: Person,
    school_id: number,
    school_id_fk: School,
    owner_login: string,
    record_acl: string,
    person_comment_created: string,
    person_comment_modified: string,
    person_comment_deleted: string,
    person_comment_changedby: string,
}

export interface PersonCommentList {
    values: PersonComment[],
    length: number
}

export interface Submission {
    submission_id: number,
    mail: string,
    attachment: string,
    fileexchange: string,
    submission_timestamp: string,
    sender: string,
    replied: string,
    processed: string,
    contest_year: string,
}

export interface SubmissionList {
    values: Submission[],
    length: number
}

export interface Contestants {
    contestants_id: number,
    name: string,
    mail: string,
    phone: string,
    parents: string,
    address: string,
    school: string,
    level: string,
    teacher_name: string,
    work: string,
    fileexchange: string,
    status: string,
    contest_year: string,
    solutions_list: SolutionsList,
}

export interface ContestantsList {
    values: Contestants[],
    length: number
}

export interface Problems {
    problems_id: number,
    contest_year: string,
    problem_name: string,
    problem_html: string,
    people: string,
    criteria: string,
    solutions_list: SolutionsList,
}

export interface ProblemsList {
    values: Problems[],
    length: number
}

export interface Solutions {
    solutions_id: number,
    problem_id: number,
    problem_id_fk: Problems,
    contest_year: string,
    contestant_id: number,
    contestant_id_fk: Contestants,
    resolution_text: string,
    resolution_author: string,
    resolution_mark: string,
}

export interface SolutionsList {
    values: Solutions[],
    length: number
}

