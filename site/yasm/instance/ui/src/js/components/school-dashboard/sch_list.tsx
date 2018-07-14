import * as React from "react";
import {School, SchoolList} from "../../generated/interfaces";
import {callbackify} from "util";
import {SchoolCard} from "../common/SchoolCard";
import {school_list} from "../../generated/api_connect";
import {Spinner} from "../common/Spinner";
import '../../../scss/school.scss'


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
    prefix?: string
}

interface SchListState {
    sch_list: SchoolList
}


export class SchList extends React.Component<SchListProps, SchListState> {
    constructor(props: any) {
        super(props);
        school_list().then((value: SchoolList) => {
            this.setState({sch_list: value})
        })
    }
    render_list() {
        let ans = [];
        for (let i = this.state.sch_list.length - 1; i >= 0; --i) {
            ans.push(<SchoolCard title={this.state.sch_list.values[i].school_title}
                                 dates={this.state.sch_list.values[i].school_date_start + " - " + this.state.sch_list.values[i].school_date_end}
                                 place={this.state.sch_list.values[i].school_location}
                                 emblem={"/static/emblems/events/" + this.state.sch_list.values[i].school_type + ".jpg"}
                                 callback={() => {this.choose(i)}}
                                 style={{
                                     display: "flex",
                                     justifyContent: "left"
                                 }}/>);
        }
        return ans;
    }

    choose(i: number) {
        location.replace(this.props.prefix + '/' + this.state.sch_list.values[i].school_id)
    }

    render() {
        return (this.state) ? <div className="list">
            {this.render_list()}
        </div> : <Spinner/>
    }
}