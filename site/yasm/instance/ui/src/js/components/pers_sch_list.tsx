import * as React from "react";
import {PersonSchoolList} from "../generated/interfaces";

export interface PSListProps {
    psl: PersonSchoolList
}

export class PersSchList extends React.Component<PSListProps, undefined> {
    render_list() {
        let list = [];
        for (let i = 0; i < this.props.psl.length; ++i) {
            list.push(
                <div key={i}>
                    {this.props.psl.values[i].member_person_id_fk.first_name}
                </div>
            );
        }
        return list
    }

    render() {
        return <div className="list">
            {this.render_list()}
        </div>
    }
}