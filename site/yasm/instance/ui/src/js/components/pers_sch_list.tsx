import * as React from "react";
import {PersonSchoolList} from "../generated/interfaces";

export interface PSListProps {
    psl: PersonSchoolList
}

export class PersSchList extends React.Component<PSListProps, undefined> {
    render() {
        console.log(this.props);
        let list = [];
        for (let i = 0; i < this.props.psl.length; ++i) {
            console.log(this.props.psl.values[i]);
            list.push(
                <div>
                    {this.props.psl.values[i].member_person_id_fk.first_name}
                </div>
            );
        }
        return list
    }
}