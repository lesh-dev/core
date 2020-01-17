import { call } from "../axios";

export function fetchPerson(id: number) {
    return call(
        `/i/api/fetch_person`,
        {
            id: id,
        }
    )
}