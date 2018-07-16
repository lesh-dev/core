import * as React from 'react'
import "../../../scss/school_card/school_card.scss"
import {CSSProperties} from "react";
import {School} from "../../generated/interfaces";
import {redirect} from "./utils";

export interface SchoolCardProps {
    school: School
    clickable?: boolean
    style?: CSSProperties
}

export class SchoolCard extends React.Component<SchoolCardProps> {
    render() {
        return <div className="school_card" style={this.props.style} onClick={() => {
            if (this.props.clickable)
                redirect('/admin/gui/schools/' + this.props.school.school_id)
        }}>
            <img src={"/static/emblems/events/" + this.props.school.school_type + ".jpg"} className="school_card__img"/>
            <div className="school_card__title">{this.props.school.school_title}</div>
            <div className="school_card__meta">
                <div
                    className="school_card__meta__name">{this.props.school.school_date_start + " - " + this.props.school.school_date_end}</div>
                <div className="school_card__meta__nick">{this.props.school.school_location}</div>
            </div>
        </div>
    }
}