import * as React from "react";
import {PersonList, School, SchoolList} from "../../generated/interfaces";
import {callbackify} from "util";
import {SchoolCard} from "../common/SchoolCard";
import {person_list, school_list} from "../../generated/api_connect";
import {Spinner} from "../common/Spinner";
import '../../../scss/school.scss'
import {PersonCard} from "../common/PersonCard";


interface SLEntryProps {
    sch: School
    callback: () => void
}

class SLEntry extends React.Component<SLEntryProps> {
    render() {
        return <div onClick={() => this.props.callback()}>{this.props.sch.school_title}</div>
    }

}

export interface PersListProps {
    prefix?: string
}

interface PersListState {
    pers_list: PersonList
}


export class PersList extends React.Component<PersListProps, PersListState> {
    constructor(props: any) {
        super(props);
        person_list().then((value: PersonList) => {
            this.setState({pers_list: value})
        })
    }
    render_list() {
        let ans = [];
        for (let i = 0; i < this.state.pers_list.length; ++i) {
            ans.push(<PersonCard name={this.state.pers_list.values[i].last_name + ' ' + this.state.pers_list.values[i].first_name}
                                 nick={this.state.pers_list.values[i].nick_name}
                                 img={"https://s.hdnux.com/photos/53/27/02/11366561/5/920x920.jpg"}
                                 callback={() => {this.choose(i)}}
                                 style={{
                                     display: "flex",
                                     justifyContent: "left"
                                 }}/>);
        }
        return ans;
    }

    choose(i: number) {
        location.replace(this.props.prefix + '/' + this.state.pers_list.values[i].person_id)
    }

    render() {
        return (this.state) ? <div className="list">
            {this.render_list()}
        </div> : <Spinner/>
    }
}