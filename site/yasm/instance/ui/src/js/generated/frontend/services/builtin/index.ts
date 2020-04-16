import { AxiosResponse } from 'axios'

import * as interfaces from '../../interfaces'
import { call } from '../index'

export {

}


export namespace APIBuiltin {
        export function Search(
        data: interfaces.builtin.SearchRequest,
        headers: {[index: string]: string} = {}
    ): Promise<AxiosResponse<interfaces.builtin.SearchResponse>> {
        return call(
            '/api/builtin/APIBuiltin/Search',
            data,
            headers,
        )
    }

}

