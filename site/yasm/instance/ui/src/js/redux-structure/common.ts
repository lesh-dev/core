import { Action, createActions, handleActions, ReducerMap } from 'redux-actions'
import {Person} from "../generated/interfaces";

import { call } from '../api/axios'

export interface LoginState {
    profile?: Person,
    loggedIn?: boolean,
    loading?: boolean,
    error?: Error,
}

export interface QuestMasterState {
    opened?: boolean,
}
export interface CommonState {
    login?: LoginState,
    questMaster?:QuestMasterState
}

export const loginInitialState = {
    loggedIn: false,
    loading: false,
} as LoginState

export const questMasterInitialState = {
    opened: false,
}

export const commonInitialState = {
    login: loginInitialState,
    questMaster: questMasterInitialState,
} as CommonState

export const commonActions = createActions({
    common: {
        login: {
            fetch: () => {
                return call('/i/api/get_profile').then(resp => resp.data)
            }
        },
        questMaster: {
            toggle: () => undefined,
        }
    }
}) as any

export const loginReducer = handleActions(
    ({
        common: {
            login: {
                fetch_PENDING: (state: LoginState) => (
                    {
                        ...state,
                        loading: true,
                        error: undefined,
                    }
                ),
                fetch_FULFILLED: (state: LoginState, action: Action<Person>) => (
                    {
                        loggedIn: true,
                        loading: false,
                        profile: action.payload,
                    }
                ),
                fetch_REJECTED: (state: LoginState, action: Action<Error>) => (
                    {
                        loggedIn: false,
                        loading: false,
                        error: action.payload
                    }
                ),
            },
        }
    }) as ReducerMap<LoginState, Action<any>>,
    loginInitialState,
)

export const questMasterReducer = handleActions(
    ({
        common: {
            questMaster: {
                toggle: (state: QuestMasterState, action: Action<any>) => (
                    {
                        ...state,
                        opened: !state.opened,
                    }
                )
            },
        }
    }) as ReducerMap<QuestMasterState, Action<any>>,
    questMasterInitialState,
)

export const commonReducer = {
    common: {
        questMaster: questMasterReducer,
        login: loginReducer,
    }
}
