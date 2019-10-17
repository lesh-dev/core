import * as React from "react";
import * as ReactDOM from "react-dom";
import {LoginPocket} from "../components/common/LoginPocket";
import {BasePage} from "./base";

class LoginPage extends React.Component {
    render() {
        return <LoginPocket/>
    }
}


ReactDOM.render((
    <BasePage page_renderer={() => <LoginPage/>}/>
), document.getElementById('mount-point'));
