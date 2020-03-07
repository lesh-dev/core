import { AxiosResponse } from 'axios'

import * as interfaces from '../../../../interfaces'
import { call } from '../../../index'

export {

}


export namespace APIMisc {
        export function Search(
        data: interfaces.yasm.internal.misc.SearchRequest,
        headers: {[index: string]: string} = {}
    ): Promise<AxiosResponse<interfaces.yasm.internal.misc.SearchResponse>> {
        return call(
            '/apiyasm/internal/misc/APIMisc/Search',
            data,
            headers,
        )
    }

}

