import * as interfaces from '../../../index'

export {

}


    export namespace SearchRequest {
                    }
    export interface SearchRequest {
                    query?: string
            }


    export namespace SearchResult {
                                    type DataEntry = {[index: string]: string}
                                }
    export interface SearchResult {
                    search_url?: string
                    data?: interfaces.yasm.internal.misc.SearchResult.DataEntry
            }


    export namespace SearchResponse {
                    }
    export interface SearchResponse {
                    query?: string
                    results?: interfaces.yasm.internal.misc.SearchResult[]
            }

