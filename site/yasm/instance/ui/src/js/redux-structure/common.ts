import { Action, createActions, handleActions, ReducerMap } from 'redux-actions'
import {Ava, Contact, Person} from "../generated/frontend/interfaces/yasm/database";

import { SidebarState, getReducer as getSidebarReducer, getInitialState as getSidebarInitialState } from './sidebar'
import { history } from '../util/history'
import { APIPersonal } from '../generated/frontend/services/yasm/internal/person'
import {ContactsPatch, ContactList, GetProfileResponse} from '../generated/frontend/interfaces/yasm/internal/person'

export enum TopRightPanels {
    NONE,
    PERSONAL,
    QUESTS,
}

export interface LoginState {
    profile?: Person & GetProfileResponse,
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
    sidebar?: SidebarState,
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

export const commonActions = createActions({
    common: {
        login: {
            fetchInit: (onlyLogin: boolean = true) => {
                if (onlyLogin) {
                    return APIPersonal.GetProfile({}).then(resp => resp.data)
                }
                return APIPersonal.GetProfileInfo({}).then(resp => resp.data)
            },
            fetch: () => {
                return APIPersonal.GetProfile({}).then(resp => resp.data)
            },
            setAva: (ava: string) => APIPersonal.SetAva({new_ava: ava}).then(resp => resp.data),
            patchContacts: (contactPatch: ContactsPatch) => APIPersonal.PatchContacts(contactPatch).then(resp => resp.data),
            exit: () => history.push('/login/logout'),
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
                setAva_PENDING: (state: LoginState) => (
                    {
                        ...state,
                        error: undefined,
                    }
                ),
                setAva_FULFILLED: (state: LoginState, action: Action<Ava>) => (
                    {
                        ...state,
                        profile: {
                            ...state.profile,
                            ava: action.payload.repr,
                        },
                    }
                ),
                setAva_REJECTED: (state: LoginState, action: Action<Error>) => (
                    {
                        ...state,
                        error: action.payload,
                    }
                ),
                fetchInit_PENDING: (state: LoginState) => (
                    {
                        ...state,
                        loading: true,
                        error: undefined,
                    }
                ),
                fetchInit_FULFILLED: (state: LoginState, action: Action<Person>) => (
                    {
                        ...state,
                        loggedIn: true,
                        loading: false,
                        profile: {
                            ...state.profile,
                            ...action.payload
                        },
                    }
                ),
                fetchInit_REJECTED: (state: LoginState, action: Action<Error>) => (
                    {
                        ...state,
                        loading: false,
                        error: action.payload,
                    }
                ),
                fetch_PENDING: (state: LoginState) => (
                    {
                        ...state,
                        error: undefined,
                    }
                ),
                fetch_FULFILLED: (state: LoginState, action: Action<Person>) => (
                    {
                        ...state,
                        loggedIn: true,
                        profile: {
                            ...state.profile,
                            ...action.payload
                        },
                    }
                ),
                fetch_REJECTED: (state: LoginState, action: Action<Error>) => (
                    {
                        ...state,
                        error: action.payload,
                    }
                ),
                patchContacts_PENDING: (state: LoginState) => (
                    {
                        ...state,
                        error: undefined,
                    }
                ),
                patchContacts_FULFILLED: (state: LoginState, action: Action<ContactList>) => (
                    {
                        ...state,
                        profile: {
                            ...state.profile,
                            contacts: action.payload.contacts,
                        },
                    }
                ),
                patchContacts_REJECTED: (state: LoginState, action: Action<Error>) => (
                    {
                        ...state,
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
                        ...state,
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

export interface reducerProps {
    sidebar?: SidebarState
}

export function getReducer(props: reducerProps) {
    return {
        common: {
            panel: {
                topRight: topRightPanelReducer,
            },
            login: loginReducer,
            sidebar: getSidebarReducer(props.sidebar),
        }
    }
}

export function getInitialState(props: reducerProps): CommonState {
    return {
        sidebar: getSidebarInitialState(props.sidebar),
        panel: panelInitialState,
        login: loginInitialState,
    }
}

