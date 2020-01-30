import * as interfaces from '../../../../interfaces'
import { call } from '../../../index'

export {

}


export namespace APICourse {
        export function PatchTeachers(
        data: interfaces.yasm.internal.course.PatchTeachersRequest,
        headers: {[index: string]: string} = {}
    ): interfaces.yasm.database.Course {
        return call(
            '/api/yasm/internal/course/APICourse/PatchTeachers',
            data,
            headers,
        )
    }

        export function TMP(
        data: interfaces.yasm.database.Course.Message,
        headers: {[index: string]: string} = {}
    ): interfaces.yasm.database.Course.NestedMessage {
        return call(
            '/api/yasm/internal/course/APICourse/TMP',
            data,
            headers,
        )
    }

}

