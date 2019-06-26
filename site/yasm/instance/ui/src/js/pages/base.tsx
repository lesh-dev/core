import * as React from "react";
import {Provider} from 'react-redux'
import {applyMiddleware, combineReducers, createStore} from "redux";
import {composeWithDevTools} from "redux-devtools-extension";
import thunkMiddleware from "redux-thunk";
import {createLogger} from "redux-logger";
import {TopMenu} from "../components/common/TopMenu";
import {profileReducer} from "../redux-structure/reducers/profile";
import thunk from "redux-thunk";
import {BrowserRouter} from "react-router-dom";

interface BasePageProps {
    page_renderer: () => JSX.Element
    reducer?: any
    preloadedState?: any
}

export class BasePage extends React.Component<BasePageProps> {
    static defaultProps = {
        reducer: (state: any) => {
            if (state === undefined) {
                return null;
            } else {
                return state;
            }
        }
    };

    private readonly store: any;

    constructor(props: BasePageProps) {
        super(props);
        let enhancer: any;
        if (process.env.NODE_ENV === 'development')
            enhancer = composeWithDevTools(applyMiddleware(thunk, createLogger()));
        else
            enhancer = applyMiddleware(thunk);
        this.store = createStore(
            combineReducers({
                PROFILE: profileReducer,
                OTHERS: this.props.reducer
            }),
            this.props.preloadedState,
            enhancer
        )
    }

    render() {
        return (
            <Provider store={this.store}>
                <BrowserRouter>
                    <React.Fragment>
                        <TopMenu/>
                        {this.props.page_renderer()}
                    </React.Fragment>
                </BrowserRouter>
            </Provider>
        )
    }
}
