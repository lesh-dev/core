import * as React from "react";
import {SchoolList} from "../generated/interfaces";

export interface SchListProps {
    sch_list: SchoolList
}

export class SchList extends React.Component<SchListProps> {
    render() {
        let ans = [];
        for (let i = 0; i < this.props.sch_list.length; ++i) {
            ans.push(<div>{this.props.sch_list.values[i].school_title}</div>);
        }
        return ans;
    }
}