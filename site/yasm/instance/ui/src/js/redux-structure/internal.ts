import { Action, createActions, handleActions, ReducerMap } from 'redux-actions'

import { call } from '../api/axios'
import {Course, CourseTeachers, Person} from '../generated/interfaces'
import { APICourse } from '../generated/frontend/services/yasm/internal/course'
import { APIPeople } from '../generated/frontend/services/yasm/internal/person'
import * as interfaces from "../generated/frontend/interfaces";

export interface InternalCoursesState {
    list?: Course[],
    loading?: boolean,
    error?: Error,
}

export interface InternalPersonState {
    profile?: Person,
    loading?: boolean,
    error?: Error,
}

export interface InternalCourseState {
    course?: Course,
    loading?: boolean,
    error?: Error,
}

export interface InternalState {
    courses?: InternalCoursesState,
    person?: InternalPersonState,
    course?: InternalCourseState,
}

export const coursesInitialState = {
    loading: false,
} as InternalCoursesState

export const personInitialState = {
    loading: false,
} as InternalPersonState

export const courseInitialState = {
    loading: false,
} as InternalCoursesState

export const internalInitialState = {
    courses: coursesInitialState,
    person: personInitialState,
    course: courseInitialState,
} as InternalState

export const internalActions = createActions({
    internal: {
        courses: {
            fetch: () => {
                return call('/i/api/courses').then(resp => resp.data)
            },
        },
        person: {
            fetch: (id: number) => APIPeople.FetchPerson(id).then(resp => resp.data),
        },
        course: {
            fetch: (id: number) => APICourse.FetchCourse(id).then(resp => resp.data),
            patchTeachers: (id: number, patch: interfaces.yasm.internal.course.PatchTeachersRequest.PatchEntry) => {
                return APICourse.PatchTeachers({
                    id,
                    patch
                }).then(resp => resp.data);
            },
        }
    }
}) as any

export const coursesReducer = handleActions(
    ({
        internal: {
            courses: {
                fetch_PENDING: (state: InternalCoursesState) => (
                    {
                        ...state,
                        loading: true,
                        error: undefined,
                    }
                ),
                fetch_FULFILLED: (state: InternalCoursesState, action: Action<Course[]>) => (
                    {
                        loading: false,
                        list: action.payload,
                    }
                ),
                fetch_REJECTED: (state: InternalCoursesState, action: Action<Error>) => (
                    {
                        loading: false,
                        error: action.payload
                    }
                ),
            },
        }
    }) as ReducerMap<InternalCoursesState, Action<any>>,
    coursesInitialState,
)

export const personReducer = handleActions(
    ({
        internal: {
            person: {
                fetch_PENDING: (state: InternalPersonState) => (
                    {
                        ...state,
                        loading: true,
                        error: undefined,
                    }
                ),
                fetch_FULFILLED: (state: InternalPersonState, action: Action<Person>) => (
                    {
                        ...state,
                        error: undefined,
                        loading: false,
                        profile: action.payload,
                    }
                ),
                fetch_REJECTED: (state: InternalPersonState, action: Action<Error>) => (
                    {
                        ...state,
                        profile: undefined,
                        loading: false,
                        error: action.payload
                    }
                ),
            },
        }
    }) as ReducerMap<InternalPersonState, Action<any>>,
    personInitialState,
)

export const courseReducer = handleActions(
    ({
        internal: {
            course: {
                fetch_PENDING: (state: InternalCourseState) => (
                    {
                        ...state,
                        loading: true,
                        error: undefined,
                    }
                ),
                fetch_FULFILLED: (state: InternalCourseState, action: Action<Course>) => (
                    {
                        ...state,
                        error: undefined,
                        loading: false,
                        course: action.payload,
                    }
                ),
                fetch_REJECTED: (state: InternalCourseState, action: Action<Error>) => (
                    {
                        ...state,
                        course: undefined,
                        loading: false,
                        error: action.payload
                    }
                ),
                patchTeachers_PENDING: (state: InternalCourseState) => (
                    {
                        ...state,
                        error: undefined,
                    }
                ),
                patchTeachers_FULFILLED: (state: InternalCourseState, action: Action<CourseTeachers[]>) => (
                    {
                        ...state,
                        error: undefined,
                        course: {
                            ...state.course,
                            course_teachers: action.payload
                        },
                    }
                ),
                patchTeachers_REJECTED: (state: InternalCourseState, action: Action<Error>) => (
                    {
                        ...state,
                        error: action.payload
                    }
                ),
            },
        }
    }) as ReducerMap<InternalPersonState, Action<any>>,
    courseInitialState,
)



export const internalReducer = {
    internal: {
        courses: coursesReducer,
        person: personReducer,
        course: courseReducer,
    }
}
