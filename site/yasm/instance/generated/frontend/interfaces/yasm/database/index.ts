import * as interfaces from '../../index'

export {

}


    export namespace Person {
                    }
    export interface Person {
                    person_id?: number
                    first_name?: string
                    courses?: interfaces.yasm.database.CourseTeacher[]
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
                    teachers?: interfaces.yasm.database.CourseTeacher[]
            }


    export namespace CourseTeacher {
                    }
    export interface CourseTeacher {
                    person?: interfaces.yasm.database.Person
                    course?: interfaces.yasm.database.Course
            }


    export namespace B {
                    }
    export interface B {
                    id?: number
                    a?: interfaces.yasm.database.A
                    a2?: interfaces.yasm.database.A
            }


    export namespace A {
                    }
    export interface A {
                    id?: number
                    id2?: string
                    t?: string
                    b?: interfaces.yasm.database.B
                    c?: interfaces.yasm.database.C[]
                    d?: interfaces.yasm.database.D[]
                    e?: interfaces.yasm.database.E
                    b2?: interfaces.yasm.database.B
            }


    export namespace C {
                    }
    export interface C {
                    id?: number
                    a?: interfaces.yasm.database.A
            }


    export namespace D {
                    }
    export interface D {
                    id?: number
                    a?: interfaces.yasm.database.A
            }


    export namespace E {
                    }
    export interface E {
                    id?: number
                    a?: interfaces.yasm.database.A[]
            }


    export enum RegularEnum {
                    Z = 'Z',
                    X = 'X',
                    V = 'V',
            }

