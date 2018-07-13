import * as React from "react";
import * as ReactDOM from "react-dom";
import {BrowserRouter} from "react-router-dom";
import {SideMenu} from "../components/common/SideMenu";
import {Schools} from "./schools";

const prefix = '/admin/gui';

const App = () => (
    <div style={{display: "flex"}}>
        <SideMenu entries={[
            {
                url: prefix + '/schools',
                label: 'События'
            },
            {
                url: prefix + '/people',
                label: 'Люди'
            }
        ]}/>
        <div style={{flexGrow: 1}}><Schools/></div>
    </div>
);


ReactDOM.render((
    <BrowserRouter>
        <App/>
    </BrowserRouter>
), document.getElementById('mount-point'));