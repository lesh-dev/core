import {Person} from "../../../generated/interfaces";

export const PROFILE_LOADED = "PROFILE_LOADED";
export const PROFILE_UPDATED = "PROFILE_UPDATED";

export function profileLoaded(p: Person) {
    return {
        type: PROFILE_LOADED,
        profile: p,
    }
}

export function profileUpdated(p: Person) {
    return {
        type: PROFILE_UPDATED,
        profile: p,
    }
}
