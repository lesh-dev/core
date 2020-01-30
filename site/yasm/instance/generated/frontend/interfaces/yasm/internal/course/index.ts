import * as interfaces from '../../../index'

export {

}


    export namespace PatchTeachersRequest {
                    }
    export interface PatchTeachersRequest {
                    course_id?: number
                    teachers?: interfaces.yasm.database.Person[]
                    msg?: interfaces.yasm.database.Message
                    msg2?: interfaces.yasm.database.Course.Message
            }

