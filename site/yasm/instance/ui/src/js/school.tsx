import * as React from "react";
import * as ReactDOM from "react-dom";
import {SideMenu} from "./components/side_menu";
import {SchList} from "./components/sch_list";
import {school_list} from "./generated/api_connect";
import {School, SchoolList} from "./generated/interfaces";

interface PageState {
    chosen_school: number
    sch_list: SchoolList
}

export class Page extends React.Component<undefined, PageState> {
    constructor(props: any) {
        super(props);
        this.state = {
            sch_list: {
                length: 0,
                values: []
            },
            chosen_school: 0
        };
        school_list().then((value) => {
                console.log(value);
                this.setState({sch_list: value, chosen_school: 0})
            }
        ).catch((error) =>
            console.log("error")
        )
    }

    render_content() {
        if (this.state.chosen_school == 0) {
            return <SchList sch_list={this.state.sch_list}/>
        } else {
            return <div></div>
        }
    }

    render() {
        return [
            <SideMenu entries={[]}/>,
            this.render_content()
        ];
    }
}

ReactDOM.render(
    <Page/>,
    document.getElementById("mount-point")
);