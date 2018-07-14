import {getRequest} from "../generated/api_connect";

export function notification_list(req: number) {
    return getRequest('/api/uninvited/' + req)
}
