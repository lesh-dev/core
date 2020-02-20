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
            }


    export namespace Department {
                    }
    export interface Department {
                    id?: number
                    people?: interfaces.yasm.database.Person[]
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

