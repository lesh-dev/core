import * as interfaces from '../../../../interfaces'
import { call } from '../../../index'

export {

}


export namespace APICourse {
        export function PatchTeachers(
        data: interfacesyasm.internal.test.PatchTeachersRequest,
        headers: {[index: string]: string} = {}
    ): interfacesyasm.database.Course {
        return call(
            '/apiyasm/internal/test/APICourse/PatchTeachers',
            data,
            headers,
        )
    }

        export function TMP(
        data: interfacesyasm.database.Course.Message,
        headers: {[index: string]: string} = {}
    ): interfacesyasm.database.Course.NestedMessage {
        return call(
            '/apiyasm/internal/test/APICourse/TMP',
            data,
            headers,
        )
    }

}

