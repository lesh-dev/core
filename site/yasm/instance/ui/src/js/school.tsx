import * as React from "react";
import * as ReactDOM from "react-dom";
import {SideMenu} from "./components/side_menu";
import {BasePage} from "./index";

interface SchoolListProps {

}

class SchoolList extends React.Component<SchoolListProps> {

}

interface PageState {
    chosen_school:
}
export class Page extends React.Component<undefined, undefined> {
    render_content() {

    }
    render() {
        return [
            <SideMenu entries={}/>,
            this.render_content()
        ];
    }
}

ReactDOM.render(
    <Page compiler="TypeScript" framework="React" />,
    document.getElementById("mount-point")
);