import * as React from "react";
import {Department, DepartmentList} from "../../generated/interfaces";
import {department_list} from "../../generated/api_connect";
import {Spinner} from "../common/Spinner";
import {DepartmentCard} from "../common/Cards/DepartmentCard";
import Async from "react-promise";
import {List} from "../common/List";


interface DepsListState {
    list: DepartmentList
}


export class DepsList extends React.Component<undefined, DepsListState> {
    constructor(props: any) {
        super(props);
        department_list().then(
            value => {this.setState({list: value})},
            error => {console.log(error)}
            )
    }
    render() {
        if (this.state) {
            return <List renderer={(department: Department) => {
                return <DepartmentCard department={department}
                                       style={{
                                           display: "flex",
                                           justifyContent: "left"
                                       }}
                                       clickable={true}
                />
            }}
                         data={this.state.list.values}/>
        } else {
            return <Spinner/>
        }
    }
}