import * as interfaces from '../../../index'

export {

}


    export namespace FetchCourseRequest {
                    }
    export interface FetchCourseRequest {
                    id?: number
            }


    export namespace TeachersPatchEntry {
                    }
    export interface TeachersPatchEntry {
                    name?: string
                    action?: interfaces.yasm.internal.course.TeachersPatchActions
            }


    export namespace PatchTeachersRequest {
                                    type PatchEntry = {[index: number]: interfaces.yasm.internal.course.TeachersPatchEntry}
                                }
    export interface PatchTeachersRequest {
                    id?: number
                    patch?: interfaces.yasm.internal.course.PatchTeachersRequest.PatchEntry
            }


    export namespace PatchTeachersResponse {
                    }
    export interface PatchTeachersResponse {
                    teachers?: interfaces.yasm.database.Person[]
            }


    export enum TeachersPatchActions {
                    add = 'add',
                    remove = 'remove',
            }

