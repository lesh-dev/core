import * as interfaces from '../../../../interfaces'
import { call } from '../../../index'

export {

}


export namespace APICourse {
        export function PatchTeachers(
        data: interfaces<google.protobuf.pyext._message.MessageDescriptor object at 0x7f60581a3e80>,
        headers: {[index: string]: string} = {}
    ): interfaces<google.protobuf.pyext._message.MessageDescriptor object at 0x7f60581a3710> {
        return call(
            '/apiyasm/internal/course/APICourse/PatchTeachers',
            data,
            headers,
        )
    }

        export function TMP(
        data: interfaces<google.protobuf.pyext._message.MessageDescriptor object at 0x7f6058170be0>,
        headers: {[index: string]: string} = {}
    ): interfaces<google.protobuf.pyext._message.MessageDescriptor object at 0x7f60581a36d8> {
        return call(
            '/apiyasm/internal/course/APICourse/TMP',
            data,
            headers,
        )
    }

}

