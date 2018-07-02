import * as React from "react";
import * as ReactDOM from "react-dom";
import {SideMenu} from "./components/side_menu";

export class BasePage extends React.Component<undefined, undefined> {
    render_content() {}
    render() {
        return [
            <SideMenu entries={}/>,
            this.render_content()
        ];
    }
}
