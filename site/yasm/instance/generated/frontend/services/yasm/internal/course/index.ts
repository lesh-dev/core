import * as interfaces from '../../../../interfaces'
import { call } from '../../../index'

export {

}


export namespace APICourse {
        export function PatchTeachers(
        data: interfaces.yasm.internal.course.PatchTeachersRequest,
        headers: {[index: string]: string} = {}
    ): interfaces.google.protobuf.Empty {
        return call(
            '/apiyasm/internal/course/APICourse/PatchTeachers',
            data,
            headers,
        )
    }

}

