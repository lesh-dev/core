import * as React from "react";
import * as ReactDOM from "react-dom";
import {BasePage} from "./base";
import {Route, Switch} from "react-router";
import {Personal} from "./internal/personal";


class Internal extends React.Component {
    render(): React.ReactNode {
        return (
            <Switch>
                <Route
                    path={'/i/'}
                    exact
                    render={() => <Personal/>}
                />
            </Switch>
        )
    }
}


ReactDOM.render((
    <BasePage>
        <Internal/>
    </BasePage>
), document.getElementById('mount-point'));
