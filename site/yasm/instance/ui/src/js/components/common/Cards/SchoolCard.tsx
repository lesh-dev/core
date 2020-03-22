import * as React from 'react'
import "../../../../scss/cards/school_card/school_card.scss"
import {CSSProperties} from "react";
import {School} from "../../../generated/frontend/interfaces/yasm/database";
import {redirect} from "../utils";

export interface SchoolCardProps {
    school: School
    clickable?: boolean
    callback?: () => void
    style?: CSSProperties
}

export class SchoolCard extends React.Component<SchoolCardProps> {
    render() {
        return <div className={"school_card" + (this.props.clickable ? " school_card--clickable" : "")}
                    style={this.props.style} onClick={() => {
            if (this.props.clickable) {
                if (!this.props.callback)
                    redirect('/admin/gui/schools/' + this.props.school.id)
                else
                    this.props.callback()
            }
        }}>
            <img src={"/static/emblems/events/" + this.props.school.type + ".jpg"} className="school_card__img"/>
            <div className="school_card__title">{this.props.school.title}</div>
            <div className="school_card__meta">
                <div
                    className="school_card__meta__name">{this.props.school.start + " - " + this.props.school.end}</div>
                <div className="school_card__meta__nick">{this.props.school.location}</div>
            </div>
        </div>
    }
}