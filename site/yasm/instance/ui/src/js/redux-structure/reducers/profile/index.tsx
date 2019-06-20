import * as actions from "../../actions/profile";

export function profileReducer(state: any, action: any) {
    if (state !== undefined) {
        let newState = state;

        switch (action.type) {
            case actions.PROFILE_LOADED:
                newState = action.profile;
                return newState;
            case actions.PROFILE_UPDATED:
                newState = {...newState, ...action.profile};
                return newState;
            default:
                return state;
        }
    } else {
        return null;
    }
}
