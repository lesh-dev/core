import * as React from "react";
import {School} from "../generated/interfaces";
import {PersSchList} from "./pers_sch_list";

export interface SchProps {
    sch: School
}

export class Sch extends React.Component<SchProps, undefined> {
    render() {
        return [
            <div>{this.props.sch.school_title}</div>,
            <PersSchList psl={this.props.sch.person_school_list}/>
        ]
    }
}