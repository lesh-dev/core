import { Action, createActions, handleActions, ReducerMap } from 'redux-actions'

import { call } from '../api/axios'
import {Course, Person} from '../generated/interfaces'
import {fetchPerson, fetchCourse} from "../api/internal/common";

export interface CoursesState {
    list?: Course[],
    loading?: boolean,
    error?: Error,
}

export interface PersonState {
    profile?: Person,
    loading?: boolean,
    error?: Error,
}

export interface CourseState {
    course?: Course,
    loading?: boolean,
    error?: Error,
}

export interface InternalState {
    courses?: CoursesState,
    person?: PersonState,
    course?: CoursesState,
}

export const coursesInitialState = {
    loading: false,
} as CoursesState

export const personInitialState = {
    loading: false,
} as PersonState

export const courseInitialState = {
    loading: false,
} as CoursesState

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
            }
        },
        person: {
            fetch: (id: number) => fetchPerson(id).then(resp => resp.data)
        },
        course: {
            fetch: (id: number) => fetchCourse(id).then(resp => resp.data)
        }
    }
}) as any

export const coursesReducer = handleActions(
    ({
        internal: {
            courses: {
                fetch_PENDING: (state: CoursesState) => (
                    {
                        ...state,
                        loading: true,
                        error: undefined,
                    }
                ),
                fetch_FULFILLED: (state: CoursesState, action: Action<Course[]>) => (
                    {
                        loading: false,
                        list: action.payload,
                    }
                ),
                fetch_REJECTED: (state: CoursesState, action: Action<Error>) => (
                    {
                        loading: false,
                        error: action.payload
                    }
                ),
            },
        }
    }) as ReducerMap<CoursesState, Action<any>>,
    coursesInitialState,
)

export const personReducer = handleActions(
    ({
        internal: {
            person: {
                fetch_PENDING: (state: PersonState) => (
                    {
                        ...state,
                        loading: true,
                        error: undefined,
                    }
                ),
                fetch_FULFILLED: (state: PersonState, action: Action<Person>) => (
                    {
                        ...state,
                        error: undefined,
                        loading: false,
                        profile: action.payload,
                    }
                ),
                fetch_REJECTED: (state: PersonState, action: Action<Error>) => (
                    {
                        ...state,
                        profile: undefined,
                        loading: false,
                        error: action.payload
                    }
                ),
            },
        }
    }) as ReducerMap<PersonState, Action<any>>,
    personInitialState,
)

export const courseReducer = handleActions(
    ({
        internal: {
            course: {
                fetch_PENDING: (state: CoursesState) => (
                    {
                        ...state,
                        loading: true,
                        error: undefined,
                    }
                ),
                fetch_FULFILLED: (state: CoursesState, action: Action<Course>) => (
                    {
                        ...state,
                        error: undefined,
                        loading: false,
                        course: action.payload,
                    }
                ),
                fetch_REJECTED: (state: CoursesState, action: Action<Error>) => (
                    {
                        ...state,
                        course: undefined,
                        loading: false,
                        error: action.payload
                    }
                ),
            },
        }
    }) as ReducerMap<PersonState, Action<any>>,
    courseInitialState,
)



export const internalReducer = {
    internal: {
        courses: coursesReducer,
        person: personReducer,
        course: courseReducer,
    }
}
