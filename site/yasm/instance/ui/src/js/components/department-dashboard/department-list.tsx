import * as React from "react";
import {DepartmentList, PersonList, School, SchoolList} from "../../generated/interfaces";
import {callbackify} from "util";
import {SchoolCard} from "../common/SchoolCard";
import {department_list} from "../../generated/api_connect";
import {Spinner} from "../common/Spinner";
import '../../../scss/school.scss'
import {PersonCard} from "../common/PersonCard";
import {DepartmentCard} from "../common/DepartmentCard";

export interface DepListProps {
    prefix?: string
}

interface DepListState {
    deps_list: DepartmentList
}


export class DepsList extends React.Component<DepListProps, DepListState> {
    constructor(props: any) {
        super(props);
        department_list().then((value: DepartmentList) => {
            this.setState({deps_list: value})
        })
    }

    render_list() {
        let ans = [];
        for (let i = 0; i < this.state.deps_list.length; ++i) {
            ans.push(<DepartmentCard title={this.state.deps_list.values[i].department_title}
                                     emblem={"/static/emblems/departments/" + this.state.deps_list.values[i].department_id + ".jpg"}
                                     callback={() => {
                                         this.choose(i)
                                     }}
                                     style={{
                                         display: "flex",
                                         justifyContent: "left"
                                     }}/>);
        }
        return ans;
    }

    choose(i: number) {
        location.replace(this.props.prefix + '/' + this.state.deps_list.values[i].department_id)
    }

    render() {
        return (this.state) ? <div className="list">
            {this.render_list()}
        </div> : <Spinner/>
    }
}