import { AxiosResponse } from 'axios'

import * as interfaces from '../../../../interfaces'
import { call } from '../../../index'

export {

}


export namespace APICourse {
        export function FetchCourse(
        data: interfaces.yasm.internal.course.FetchCourseRequest,
        headers: {[index: string]: string} = {}
    ): Promise<AxiosResponse<interfaces.yasm.database.Course>> {
        return call(
            '/api/yasm/internal/course/APICourse/FetchCourse',
            data,
            headers,
        )
    }

        export function PatchTeachers(
        data: interfaces.yasm.internal.course.PatchTeachersRequest,
        headers: {[index: string]: string} = {}
    ): Promise<AxiosResponse<interfaces.yasm.internal.course.PatchTeachersResponse>> {
        return call(
            '/api/yasm/internal/course/APICourse/PatchTeachers',
            data,
            headers,
        )
    }

}

