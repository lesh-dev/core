import * as React from "react";
import * as ReactDOM from "react-dom";
import {SchList} from "./components/sch_list";
import {school_fill, school_list} from "./generated/api_connect";
import {School, SchoolList} from "./generated/interfaces";
import {Sch} from "./components/sch";
import {combineAll} from "rxjs/operators";

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
            chosen_school: -1
        };
        school_list().then((value) => {
                console.log(value);
                this.setState({sch_list: value})
            }
        ).catch((error) =>
            console.log("error")
        )
    }

    render() {
        if (this.state.chosen_school == -1) {
            return <SchList sch_list={this.state.sch_list} callback={(i: number) => this.choose(i)}/>
        } else {
            return <Sch sch={this.state.sch_list.values[this.state.chosen_school]}/>
        }
    }

    choose(i: number) {
        if (this.state.sch_list.values[i].person_school_list.length == 0) {
            school_fill(this.state.sch_list.values[i])
                .then((value: School) => {
                    let l = this.state.sch_list;
                    l.values[i] = value;
                    this.setState({sch_list: l});
                })
        }
        this.setState({chosen_school: i})
    }
}

ReactDOM.render(
    <Page/>,
    document.getElementById("mount-point")
);