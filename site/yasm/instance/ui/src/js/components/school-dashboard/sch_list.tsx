import * as React from "react";
import {School, SchoolList} from "../../generated/interfaces";
import {callbackify} from "util";
import {SchoolCard} from "../common/SchoolCard";


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
            ans.push(<SchoolCard title={this.props.sch_list.values[i].school_title}
                                 dates={this.props.sch_list.values[i].school_date_start + " - " + this.props.sch_list.values[i].school_date_end}
                                 place={this.props.sch_list.values[i].school_location}
                                 emblem={"https://s.hdnux.com/photos/53/27/02/11366561/5/920x920.jpg"}
                                 callback={() => {this.choose(i)}}
                                 style={{
                                     display: "flex",
                                     justifyContent: "left"
                                 }}/>);
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