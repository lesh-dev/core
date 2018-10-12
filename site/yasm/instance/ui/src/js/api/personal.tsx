import {getRequest} from "../generated/api_connect";

export function get_profile() {
    return getRequest('/personal/get_profile')
}
