import * as interfaces from '../../../../interfaces'
import { call } from '../../../index'

export {

}


export namespace APIPersonal {
        export function GetProfile(
        data: interfaces.google.protobuf.Empty,
        headers: {[index: string]: string} = {}
    ): interfaces.yasm.database.Person {
        return call(
            '/apiyasm/internal/person/APIPersonal/GetProfile',
            data,
            headers,
        )
    }

        export function GetProfileInfo(
        data: interfaces.google.protobuf.Empty,
        headers: {[index: string]: string} = {}
    ): interfaces.yasm.database.Person {
        return call(
            '/apiyasm/internal/person/APIPersonal/GetProfileInfo',
            data,
            headers,
        )
    }

        export function SetAva(
        data: interfaces.yasm.internal.person.SetAvaRequest,
        headers: {[index: string]: string} = {}
    ): interfaces.yasm.database.Ava {
        return call(
            '/apiyasm/internal/person/APIPersonal/SetAva',
            data,
            headers,
        )
    }

        export function PatchContacts(
        data: interfaces.yasm.internal.person.ContactsPatch,
        headers: {[index: string]: string} = {}
    ): interfaces.yasm.internal.person.ContactList {
        return call(
            '/apiyasm/internal/person/APIPersonal/PatchContacts',
            data,
            headers,
        )
    }

        export function SetPassword(
        data: interfaces.yasm.internal.person.SetPasswordRequest,
        headers: {[index: string]: string} = {}
    ): interfaces.google.protobuf.Empty {
        return call(
            '/apiyasm/internal/person/APIPersonal/SetPassword',
            data,
            headers,
        )
    }

        export function GetCourses(
        data: interfaces.google.protobuf.Empty,
        headers: {[index: string]: string} = {}
    ): interfaces.yasm.internal.person.CoursesResponse {
        return call(
            '/apiyasm/internal/person/APIPersonal/GetCourses',
            data,
            headers,
        )
    }

}


export namespace APIPeople {
        export function FetchPerson(
        data: interfaces.yasm.internal.person.FetchPersonRequest,
        headers: {[index: string]: string} = {}
    ): interfaces.yasm.database.Person {
        return call(
            '/apiyasm/internal/person/APIPeople/FetchPerson',
            data,
            headers,
        )
    }

}

