import * as React from "react";
import * as ReactDOM from "react-dom";
import {SchList} from "../components/school-dashboard/sch_list";
import {school_fill, school_list} from "../generated/api_connect";
import {School, SchoolList} from "../generated/interfaces";
import {SchoolDashboard} from "../components/school-dashboard/school-dashboard";
import '../../scss/school.scss'
import {Spinner} from "../components/common/Spinner";

interface PageState {
    chosen_school: number
    sch_list: SchoolList
}

export class Schools extends React.Component<undefined, PageState> {
    constructor(props: any) {
        console.log();
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
                this.setState({sch_list: value});
            }
        ).catch((error) =>
            console.log("error")
        )
    }

    render() {
        if (this.state.chosen_school == -1) {
            if (this.state.sch_list) {
                return <SchList sch_list={this.state.sch_list} callback={(i: number) => {
                    this.choose(i)
                }}/>
            } else {
                return <Spinner/>
            }
        } else {
            if (this.state.sch_list.values[this.state.chosen_school]) {
                return <SchoolDashboard sch={this.state.sch_list.values[this.state.chosen_school]} on_back={() => {
                    this.choose(-1)
                }}/>
            } else {
                return <Spinner/>
            }
        }
    }

    choose(i: number, change_path: boolean = true) {
        if (i >= 0 && this.state.sch_list.values[i].person_school_list.length == 0) {
            school_fill(this.state.sch_list.values[i])
                .then((value: School) => {
                    let l = this.state.sch_list;
                    l.values[i] = value;
                    this.setState({sch_list: l});
                });

        }
        if (change_path) {
            if (i == -1)
                window.history.pushState("", "События", "../schools")
            else
                window.history.pushState("", this.state.sch_list.values[i].school_title, "schools/" + i)
        }
        this.setState({chosen_school: i})
    }
}
