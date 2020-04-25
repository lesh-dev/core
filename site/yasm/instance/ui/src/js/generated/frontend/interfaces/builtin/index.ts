import * as interfaces from '../index'

export {

}


    export namespace SearchRequest {
                    }
    export interface SearchRequest {
                    query?: string
                    tables?: string[]
            }


    export namespace SearchResponse {
                    }
    export interface SearchResponse {
                    query?: string
                    person?: interfaces.yasm.database.Person[]
                    department?: interfaces.yasm.database.Department[]
                    school?: interfaces.yasm.database.School[]
                    course?: interfaces.yasm.database.Course[]
            }

