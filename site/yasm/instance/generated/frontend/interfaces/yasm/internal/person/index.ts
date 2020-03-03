import * as interfaces from '../../../index'

export {

}


    export namespace ContactsPatchEntry {
                    }
    export interface ContactsPatchEntry {
                    name?: string
                    action?: interfaces.yasm.internal.person.ContactsPatchActions
            }


    export namespace ContactsPatch {
                                        }
    export interface ContactsPatch {
                    entries?: {[index: string]: interfaces.yasm.internal.person.ContactsPatchEntry}
            }


    export namespace ContactList {
                    }
    export interface ContactList {
                    contacts?: interfaces.yasm.database.Contact[]
            }


    export namespace SetAvaRequest {
                    }
    export interface SetAvaRequest {
                    new_ava?: string
            }


    export namespace SetPasswordRequest {
                    }
    export interface SetPasswordRequest {
                    new_ava?: string
            }


    export namespace FetchPersonRequest {
                    }
    export interface FetchPersonRequest {
                    id?: number
            }


    export namespace CoursesResponse {
                    }
    export interface CoursesResponse {
                    courses?: interfaces.yasm.database.Course[]
            }


    export enum ContactsPatchActions {
                    add = 'add',
                    remove = 'remove',
            }

