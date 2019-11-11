import { Action, createActions, handleActions, ReducerMap } from 'redux-actions'
import {Person} from "../generated/interfaces";

import { call } from '../api/axios'

export enum TopRightPanels {
    NONE,
    PERSONAL,
    QUESTS,
}

export interface LoginState {
    profile?: Person,
    loggedIn?: boolean,
    loading?: boolean,
    error?: Error,
}

export interface TopRightPanelState {
    current?: TopRightPanels,
}

export interface PanelState {
    topRight?: TopRightPanelState,
}

export interface CommonState {
    login?: LoginState,
    panel?: PanelState,
}

export const loginInitialState: LoginState = {
    loggedIn: false,
    loading: false,
} as LoginState

export const topRightPanelInitialState: TopRightPanelState = {
    current: TopRightPanels.NONE,
}

export const panelInitialState: PanelState = {
    topRight: topRightPanelInitialState,
}

export const commonInitialState = {
    login: loginInitialState,
    panel: panelInitialState,
} as CommonState

export const commonActions = createActions({
    common: {
        login: {
            fetch: () => call('/i/api/get_profile').then(resp => resp.data),
            togglePanel: () => undefined,
            exit: () => call('/login/logout').then(resp => resp.data),
        },
        panel: {
            topRight: {
                toggle: (p: TopRightPanels) => p
            }
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
                        error: action.payload,
                    }
                ),
                exit_PENDING: (state: LoginState, action: Action<any>) => ({
                    ...state,
                    loading: true,
                }),
                exit_FULFILLED: (state: LoginState, action: Action<any>) => loginInitialState,
                exit_REJECTED: (state: LoginState, action: Action<Error>) => (
                    {
                        loggedIn: false,
                        loading: false,
                        error: action.payload,
                    }
                ),
            }
        }
    }) as ReducerMap<LoginState, Action<any>>,
    loginInitialState,
)

export const topRightPanelReducer = handleActions(
    ({
        common: {
            panel: {
                topRight: {
                    toggle: (state: TopRightPanelState, action: Action<TopRightPanels>) => {
                        if (state.current !== action.payload) {
                            return {
                                ...state,
                                current: action.payload,
                            }
                        } else {
                            return {
                                ...state,
                                current: TopRightPanels.NONE,
                            }
                        }
                    },
                },
            },
        },
    }) as ReducerMap<TopRightPanelState, Action<any>>,
    topRightPanelInitialState,
)


export const commonReducer = {
    common: {
        panel: {
            topRight: topRightPanelReducer,
        },
        login: loginReducer,
    }
}
