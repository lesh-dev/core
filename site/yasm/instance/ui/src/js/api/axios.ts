import * as axios from 'axios'

declare var csrf_token: string;

export function call(url: string, data: any = undefined, headers: any = {}) {
    return axios.default.post(
        url,
        data,
        {
            headers: {
                'X-CSRFToken': csrf_token,
                ...headers,
            }
        }
    )
}
