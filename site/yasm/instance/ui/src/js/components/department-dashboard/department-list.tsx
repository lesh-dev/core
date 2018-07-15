import * as React from "react";
import {DepartmentList} from "../../generated/interfaces";
import {department_list} from "../../generated/api_connect";
import {Spinner} from "../common/Spinner";
import '../../../scss/list/list.scss'
import {DepartmentCard} from "../common/DepartmentCard";
import {redirect} from "../common/utils";

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
            ans.push(<DepartmentCard department={this.state.deps_list.values[i]}
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
        redirect(this.props.prefix + '/' + this.state.deps_list.values[i].department_id)
    }

    render() {
        return (this.state) ? <div className="list">
            {this.render_list()}
        </div> : <Spinner/>
    }
}