export interface Notification {
    notification_id: number,
    mail_group: string,
    notification_text: string,
    notification_html: string,
}

export interface NotificationList {
    [index: number]: Notification
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
    [index: number]: Department
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
    department: Department,
    person_created: string,
    person_modified: string,
    person_changedby: string,
    course_teachers_list: CourseTeachersList,
    exam_list: ExamList,
    person_school_list: PersonSchoolList,
    person_comment_list: PersonCommentList,
}

export interface PersonList {
    [index: number]: Person
}

export interface Course {
    course_id: number,
    course_title: string,
    school_id: number,
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
    [index: number]: Course
}

export interface CourseTeachers {
    course_teachers_id: number,
    course_id: number,
    course: Course,
    course_teacher_id: number,
    person: Person,
    course_teachers_created: string,
    course_teachers_modified: string,
    course_teachers_changedby: string,
}

export interface CourseTeachersList {
    [index: number]: CourseTeachers
}

export interface Exam {
    exam_id: number,
    student_person_id: number,
    person: Person,
    course_id: number,
    course: Course,
    exam_status: string,
    deadline_date: string,
    exam_comment: string,
    exam_created: string,
    exam_modified: string,
    exam_changedby: string,
}

export interface ExamList {
    [index: number]: Exam
}

export interface School {
    school_id: number,
    school_title: string,
    school_type: string,
    school_date_start: string,
    school_date_end: string,
    school_location: string,
    school_created: string,
    school_modified: string,
    school_changedby: string,
    person_school_list: PersonSchoolList,
    person_comment_list: PersonCommentList,
}

export interface SchoolList {
    [index: number]: School
}

export interface PersonSchool {
    person_school_id: number,
    member_person_id: number,
    person: Person,
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
}

export interface PersonSchoolList {
    [index: number]: PersonSchool
}

export interface PersonComment {
    person_comment_id: number,
    comment_text: string,
    blamed_person_id: number,
    person: Person,
    school_id: number,
    school: School,
    owner_login: string,
    record_acl: string,
    person_comment_created: string,
    person_comment_modified: string,
    person_comment_deleted: string,
    person_comment_changedby: string,
}

export interface PersonCommentList {
    [index: number]: PersonComment
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
    [index: number]: Submission
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
    [index: number]: Contestants
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
    [index: number]: Problems
}

export interface Solutions {
    solutions_id: number,
    problem_id: number,
    problems: Problems,
    contest_year: string,
    contestant_id: number,
    contestants: Contestants,
    resolution_text: string,
    resolution_author: string,
    resolution_mark: string,
}

export interface SolutionsList {
    [index: number]: Solutions
}

