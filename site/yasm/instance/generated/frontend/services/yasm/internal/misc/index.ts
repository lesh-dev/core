import * as interfaces from '../../../../interfaces'
import { call } from '../../../index'

export {

}


export namespace APIMisc {
        export function Search(
        data: interfaces.yasm.internal.misc.SearchRequest,
        headers: {[index: string]: string} = {}
    ): interfaces.yasm.internal.misc.SearchResponse {
        return call(
            '/apiyasm/internal/misc/APIMisc/Search',
            data,
            headers,
        )
    }

}

