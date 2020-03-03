import * as interfaces from '../../../../interfaces'
import { call } from '../../../index'

export {

}


export namespace APICourse {
        export function FetchCourse(
        data: interfaces.yasm.internal.course.FetchCourseRequest,
        headers: {[index: string]: string} = {}
    ): interfaces.yasm.database.Course {
        return call(
            '/apiyasm/internal/course/APICourse/FetchCourse',
            data,
            headers,
        )
    }

}

