import * as React from 'react'
import "../../../../scss/tokens/school_token/school_token.scss"
import {CSSProperties} from "react";
import {School} from "../../../generated/interfaces";
import {redirect} from "../utils";

export interface SchoolCardProps {
    school: School
    clickable?: boolean
    callback?: () => void
    style?: CSSProperties
}

export class SchoolToken extends React.Component<SchoolCardProps> {
    render() {
        return <div className={"school_token" + (this.props.clickable ? " school_token--clickable" : "")}
                    style={this.props.style} onClick={() => {
            if (this.props.clickable) {
                if (!this.props.callback)
                    redirect('/admin/gui/schools/' + this.props.school.school_id)
                else
                    this.props.callback()
            }
        }}>
            <img src={"/static/emblems/events/" + this.props.school.school_type + ".jpg"} className="school_token__img"/>
            <div className="school_token__title">{this.props.school.school_title}</div>
        </div>
    }
}