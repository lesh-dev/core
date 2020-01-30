import Axios from 'axios'

declare var csrf_token: string;

export function call(url: string, data: any = undefined, headers: any = {}) {
    return Axios.post(
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
