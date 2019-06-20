import {Person} from "../../../generated/interfaces";
import {get_profile} from "../../../api/personal";
import {profileLoaded, profileUpdated} from "../../actions/profile";

export function loadProfileOnce(dispatch: (action: any) => void) {
    if (this.loading) {
        return;
    } else {
        this.loading = true;
        get_profile().then(value => {
            dispatch(profileLoaded(value));
        })
    }
}

export function updateProfile(state: Person, dispatch: (action: any) => void) {
    get_profile().then(value => {
        dispatch(profileUpdated(value));
    })
}
