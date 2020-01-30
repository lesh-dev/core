import Axios from 'axios'

declare var csrf_token: string;

export function call(
        url: string,
        data: any = undefined,
        headers: {[index: string]: string} ={}
    ) {
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

import * as yasm from './yasm'
export {

    yasm,
}

