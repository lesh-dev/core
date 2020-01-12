import { Action, createActions, handleActions, ReducerMap } from 'redux-actions'

import { call } from '../api/axios'
import { Course } from '../generated/interfaces'

export interface CoursesState {
    list?: Course[],
    loading?: boolean,
    error?: Error,
}

export interface InternalState {
    courses?: CoursesState,
}

export const coursesInitialState = {
    loading: false,
} as CoursesState

export const internalInitialState = {
    courses: coursesInitialState,
} as InternalState

export const internalActions = createActions({
    internal: {
        courses: {
            fetch: () => {
                return call('/i/api/courses').then(resp => resp.data)
            }
        },
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


export const internalReducer = {
    internal: {
        courses: coursesReducer,
    }
}
