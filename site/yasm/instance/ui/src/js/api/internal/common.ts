import { call } from "../axios";

export enum PatchAction {
    ADD,
    REMOVE,
}

export function fetchPerson(id: number) {
    return call(
        `/i/api/fetch_person`,
        {
            id: id,
        }
    )
}

export function fetchCourse(id: number) {
    return call(
        '/i/api/fetch_course',
        {
            id: id,
        }
    )

}