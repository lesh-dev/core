import * as React from "react"
import {connect, Provider, Store} from "react-redux"
import {applyMiddleware, combineReducers, createStore} from "redux"
import thunkMiddleware from 'redux-thunk'
import { createLogger } from 'redux-logger'
import { composeWithDevTools } from 'redux-devtools-extension'
import * as _ from "lodash"

import {reducer, initialState} from './attributes/reducers/AttributesReducers'
import AttributeTable from './attributes/containers/AttributeTable'


let enhancer: any;
/// #if ENV === "development"
enhancer = composeWithDevTools( applyMiddleware(thunkMiddleware, createLogger()) );
/// #else
enhancer = null;
/// #endif
const makeStore = () => createStore(reducer, initialState, enhancer);

export const ATExample = () => 
    <Provider store={makeStore()}>
        <AttributeTable school_id={20}/>
    </Provider>
