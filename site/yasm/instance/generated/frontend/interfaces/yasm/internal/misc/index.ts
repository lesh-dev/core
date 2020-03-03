import * as interfaces from '../../../index'

export {

}


    export namespace SearchRequest {
                    }
    export interface SearchRequest {
                    query?: string
            }


    export namespace SearchResult {
                                        }
    export interface SearchResult {
                    search_url?: string
                    data?: {[index: string]: string}
            }


    export namespace SearchResponse {
                    }
    export interface SearchResponse {
                    query?: string
                    results?: interfaces.yasm.internal.misc.SearchResult[]
            }

