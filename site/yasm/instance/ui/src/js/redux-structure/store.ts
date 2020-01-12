import promise from "redux-promise-middleware";
import {createLogger} from "redux-logger";
import {composeWithDevTools} from "redux-devtools-extension";
import {applyMiddleware, combineReducers, compose, createStore, ReducersMapObject} from "redux";
import { Action, ReduxCompatibleReducer } from 'redux-actions'
import { getReducer as getCommonReducer, getInitialState as getCommonInitialState, CommonState } from './common'

const productionMiddleware = [
    promise,
]

const devMiddleware = [
    ...productionMiddleware,
    createLogger({
        collapsed: true,
        diff: true,
        duration: true,
    }),
]

const composed = process.env.NODE_ENV === 'development'
    ? composeWithDevTools(applyMiddleware(...devMiddleware))
    : compose(applyMiddleware(...productionMiddleware))


export interface ReducerMap {
    [key: string]: ReducerMap | ReduxCompatibleReducer<any, Action<any>>,
}

function normalizeReducer(reducerMap: ReducerMap): ReducersMapObject {
    const reducer = {} as ReducersMapObject
    for (const prefix of Object.keys(reducerMap)) {
        if (typeof reducerMap[prefix].call !== 'function') {
            reducer[prefix] = combineReducers(normalizeReducer(reducerMap[prefix] as ReducerMap))
        } else {
            reducer[prefix] = reducerMap[prefix] as ReduxCompatibleReducer<any, Action<any>>
        }
    }
    return reducer
}

export function getStore(reducerMap: ReducerMap, initialState: any, initialCommonState: CommonState) {
    return createStore(
        combineReducers(
            {
                ...normalizeReducer(
                    reducerMap,
                ),
                ...normalizeReducer(
                    getCommonReducer(initialCommonState),
                ),
            },
        ),
        {
            ...initialState,
            common: getCommonInitialState(initialCommonState),
        },
        composed,
    )
}


export interface ReduxProps {
    dispatch?: (action: Action<any>) => void
}
