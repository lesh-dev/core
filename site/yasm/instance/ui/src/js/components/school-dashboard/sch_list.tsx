import * as React from "react";
import {School, SchoolList} from "../../generated/interfaces";
import {callbackify} from "util";


interface SLEntryProps {
    sch: School
    callback: () => void
}

class SLEntry extends React.Component<SLEntryProps> {
    render() {
        return <div onClick={() => this.props.callback()}>{this.props.sch.school_title}</div>
    }

}

export interface SchListProps {
    sch_list: SchoolList,
    callback: (i: number) => void
}


export class SchList extends React.Component<SchListProps> {
    render_list() {
        let ans = [];
        for (let i = 0; i < this.props.sch_list.length; ++i) {
            ans.push(<SLEntry sch={this.props.sch_list.values[i]} callback={() => this.choose(i)} key={i}/>);
        }
        return ans;
    }

    choose(i: number) {
        this.props.callback(i);
    }

    render() {
        return <div className="list">
            {this.render_list()}
        </div>
    }
}