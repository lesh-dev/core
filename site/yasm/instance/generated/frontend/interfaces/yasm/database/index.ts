import * as interfaces from '../../index'

export {

}


    export namespace Person {
                    }
    export interface Person {
                    person_id?: number
                    first_name?: string
            }


    export namespace Message {
                    }
    export interface Message {
            }


    export namespace Course {
                                        export namespace Message {
                    }
    export interface Message {
            }

                                                    export namespace NestedMessage {
                                                                                }
    export interface NestedMessage {
                    f1?: {[index: string]: interfaces.yasm.database.RegularEnum}
                    f2?: {[index: string]: interfaces.yasm.database.Course.NestedEnum}
                    f3?: {[index: number]: string}
            }

                                            export enum NestedEnum {
                    A = 'A',
                    B = 'B',
                    C = 'C',
            }

            }
    export interface Course {
                    course_id?: number
                    course_name?: string
                    s?: string[]
            }


    export enum RegularEnum {
                    Z = 'Z',
                    X = 'X',
                    C = 'C',
            }

