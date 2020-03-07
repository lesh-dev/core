import * as interfaces from '../../index'

export {

}


    export namespace Person {
                    }
    export interface Person {
                    id?: number
                    rights?: string
                    first_name?: string
                    last_name?: string
                    patronymic?: string
                    nick_name?: string
                    birth_date?: string
                    passport_data?: string
                    school?: string
                    school_city?: string
                    ank_class?: string
                    current_class?: string
                    phone?: string
                    cellular?: string
                    email?: string
                    skype?: string
                    social_profile?: string
                    is_teacher?: string
                    is_student?: string
                    favourites?: string
                    achievements?: string
                    hobby?: string
                    lesh_ref?: string
                    forest_1?: string
                    forest_2?: string
                    forest_3?: string
                    tent_capacity?: string
                    tour_requisites?: string
                    anketa_status?: interfaces.yasm.database.AnketaStatus
                    user_agent?: string
                    department?: interfaces.yasm.database.Department
                    person_created?: string
                    person_modified?: string
                    person_changedby?: string
                    other_contacts?: string
                    person_schools?: interfaces.yasm.database.PersonSchool[]
                    exams?: interfaces.yasm.database.Exam[]
                    courses?: interfaces.yasm.database.CourseTeachers[]
                    comments?: interfaces.yasm.database.PersonComment[]
                    avas?: interfaces.yasm.database.Ava[]
                    dlogins?: interfaces.yasm.database.DirectLogin[]
                    contacts?: interfaces.yasm.database.Contact[]
            }


    export namespace Department {
                    }
    export interface Department {
                    id?: number
                    people?: interfaces.yasm.database.Person[]
                    title?: string
                    created?: string
                    modified?: string
                    changedby?: string
                    person_schools?: interfaces.yasm.database.PersonSchool[]
            }


    export namespace PersonSchool {
                    }
    export interface PersonSchool {
                    id?: number
                    member?: interfaces.yasm.database.Person
                    department?: interfaces.yasm.database.Department
                    school?: interfaces.yasm.database.School
                    is_student?: string
                    is_teacher?: string
                    curatorship?: interfaces.yasm.database.Curatorship
                    curator_group?: string
                    courses_needed?: string
                    current_class?: string
                    comment?: string
                    created?: string
                    modified?: string
                    changedby?: string
                    arrival?: string
                    leave?: string
                    calendars?: interfaces.yasm.database.Calendar[]
            }


    export namespace Calendar {
                    }
    export interface Calendar {
                    person_school?: interfaces.yasm.database.PersonSchool
                    date?: string
                    status?: string
                    modified?: string
                    changed_by?: string
            }


    export namespace School {
                    }
    export interface School {
                    id?: number
                    title?: string
                    type?: interfaces.yasm.database.SchoolType
                    start?: string
                    end?: string
                    location?: string
                    coords?: string
                    created?: string
                    modified?: string
                    changedby?: string
                    person_schools?: interfaces.yasm.database.PersonSchool[]
                    courses?: interfaces.yasm.database.Course[]
                    person_comments?: interfaces.yasm.database.PersonComment[]
            }


    export namespace Course {
                    }
    export interface Course {
                    id?: number
                    title?: string
                    school?: interfaces.yasm.database.School
                    cycle?: string
                    target_class?: string
                    desc?: string
                    type?: interfaces.yasm.database.CourseType
                    area?: interfaces.yasm.database.CourseArea
                    created?: string
                    modified?: string
                    changedby?: string
                    teachers?: interfaces.yasm.database.CourseTeachers[]
                    exams?: interfaces.yasm.database.Exam[]
            }


    export namespace CourseTeachers {
                    }
    export interface CourseTeachers {
                    id?: number
                    course?: interfaces.yasm.database.Course
                    teacher?: interfaces.yasm.database.Person
                    created?: string
                    modified?: string
                    changedby?: string
            }


    export namespace Exam {
                    }
    export interface Exam {
                    id?: number
                    student?: interfaces.yasm.database.Person
                    course?: interfaces.yasm.database.Course
                    status?: string
                    deadline_date?: string
                    comment?: string
                    created?: string
                    modified?: string
                    changedby?: string
            }


    export namespace PersonComment {
                    }
    export interface PersonComment {
                    id?: number
                    blamed?: interfaces.yasm.database.Person
                    school?: interfaces.yasm.database.School
                    owner_login?: string
                    record_acl?: string
                    deleted?: string
                    created?: string
                    modified?: string
                    changedby?: string
            }


    export namespace Ava {
                    }
    export interface Ava {
                    id?: number
                    person?: interfaces.yasm.database.Person
                    ava?: string
                    status?: interfaces.yasm.database.DatabaseStatus
            }


    export namespace DirectLogin {
                    }
    export interface DirectLogin {
                    type?: string
                    person?: interfaces.yasm.database.Person
                    password_hash?: string
                    login?: string
            }


    export namespace Contact {
                    }
    export interface Contact {
                    id?: number
                    person?: interfaces.yasm.database.Person
                    name?: string
                    value?: string
            }


    export enum AnketaStatus {
                    progress = 'progress',
                    nextyear = 'nextyear',
                    duplicate = 'duplicate',
                    reserved = 'reserved',
                    cont = 'cont',
                    old = 'old',
                    new = 'new',
                    processed = 'processed',
                    declined = 'declined',
                    taken = 'taken',
                    duplicated = 'duplicated',
                    spam = 'spam',
                    discuss = 'discuss',
                    less = 'less',
                    verify = 'verify',
            }


    export enum Curatorship {
                    empty = 'empty',
                    none = 'none',
                    assist = 'assist',
                    cur = 'cur',
            }


    export enum SchoolType {
                    lesh = 'lesh',
                    vesh = 'vesh',
                    zesh = 'zesh',
                    summer = 'summer',
                    summmer = 'summmer',
                    winter = 'winter',
                    spring = 'spring',
            }


    export enum CourseType {
                    generic = 'generic',
                    other = 'other',
                    facult = 'facult',
                    prac = 'prac',
                    single = 'single',
            }


    export enum CourseArea {
                    cs = 'cs',
                    unknown = 'unknown',
                    nature = 'nature',
                    precise = 'precise',
                    other = 'other',
                    human = 'human',
            }


    export enum DatabaseStatus {
                    relevant = 'relevant',
                    obsolete = 'obsolete',
                    deleted = 'deleted',
            }

