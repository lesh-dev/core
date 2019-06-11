import * as React from "react";
import * as ReactDOM from "react-dom";
import {LoginPocket} from "../components/common/LoginPocket";

class LoginPage extends React.Component {
    render() {
        return <LoginPocket/>
    }
}


ReactDOM.render((
    <LoginPage/>
), document.getElementById('mount-point'));
