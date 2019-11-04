import * as React from "react";
import * as ReactDOM from "react-dom";
import {BasePage} from "./base";
import {Route, Switch} from "react-router";
import {Personal} from "./internal/Personal";
import {PersonalCourses} from "./internal/PersonalCourses";

import {internalInitialState, internalReducer} from '../redux-structure/internal'

class Internal extends React.Component {
    render(): React.ReactNode {
        return (
            <Switch>
                <Route
                    path={'/i/'}
                    exact
                    render={() => <Personal/>}
                />
                <Route
                    path={'/i/courses'}
                    exact
                    render={() => <PersonalCourses/>}
                />
            </Switch>
        )
    }
}


ReactDOM.render((
    <BasePage
        reducerMap={internalReducer}
        initialState={{
            internal: internalInitialState,
        }}
    >
        <Internal/>
    </BasePage>
), document.getElementById('mount-point'));
