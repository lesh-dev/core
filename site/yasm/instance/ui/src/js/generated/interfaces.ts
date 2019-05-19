export interface Notification {
    notification_id: number,
    mail_group: string,
    notification_text: string,
    notification_html: string,
}

export interface Department {
    department_id: number,
    department_title: string,
    department_created: string,
    department_modified: string,
    department_changedby: string,
    person: Person[],
    person_school: PersonSchool[],
}

export interface Person {
    person_id: number,
    rights: string,
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
    department: Department,
    person_created: string,
    person_modified: string,
    person_changedby: string,
    direct_login: DirectLogin[],
    contact: Contact[],
    course_teachers: CourseTeachers[],
    exam: Exam[],
    person_school: PersonSchool[],
    person_comment: PersonComment[],
}

export interface DirectLogin {
    type: string,
    person_id: number,
    person: Person,
    login: string,
    password_hash: string,
}

export interface Contact {
    id: number,
    person_id: number,
    person: Person,
    name: string,
    value: string,
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
    course: Course[],
    person_school: PersonSchool[],
    person_comment: PersonComment[],
}

export interface Course {
    course_id: number,
    course_title: string,
    school_id: number,
    school: School,
    course_cycle: string,
    target_class: string,
    course_desc: string,
    course_type: string,
    course_area: string,
    course_comment: string,
    course_created: string,
    course_modified: string,
    course_changedby: string,
    course_teachers: CourseTeachers[],
    exam: Exam[],
}

export interface CourseTeachers {
    course_teachers_id: number,
    course_id: number,
    course: Course,
    course_teacher_id: number,
    course_teacher: Person,
    course_teachers_created: string,
    course_teachers_modified: string,
    course_teachers_changedby: string,
}

export interface Exam {
    exam_id: number,
    student_person_id: number,
    student: Person,
    course_id: number,
    course: Course,
    exam_status: string,
    deadline_date: string,
    exam_comment: string,
    exam_created: string,
    exam_modified: string,
    exam_changedby: string,
}

export interface PersonSchool {
    person_school_id: number,
    member_person_id: number,
    member_person: Person,
    member_department_id: number,
    department: Department,
    school_id: number,
    school: School,
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
    calendar: Calendar[],
}

export interface Calendar {
    person_school_id: number,
    school: PersonSchool,
    date: Date,
    status: string,
    calendar_modified: number,
    changed_by: string,
}

export interface PersonComment {
    person_comment_id: number,
    comment_text: string,
    blamed_person_id: number,
    blamed_person: Person,
    school_id: number,
    school: School,
    owner_login: string,
    record_acl: string,
    person_comment_created: string,
    person_comment_modified: string,
    person_comment_deleted: string,
    person_comment_changedby: string,
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
    solutions: Solutions[],
}

export interface Problems {
    problems_id: number,
    contest_year: string,
    problem_name: string,
    problem_html: string,
    people: string,
    criteria: string,
    solutions: Solutions[],
}

export interface Solutions {
    solutions_id: number,
    problem_id: number,
    problem: Problems,
    contest_year: string,
    contestant_id: number,
    contestant: Contestants,
    resolution_text: string,
    resolution_author: string,
    resolution_mark: string,
}

