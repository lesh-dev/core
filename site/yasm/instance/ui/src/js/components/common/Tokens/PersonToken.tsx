import * as React from 'react'
import "../../../../scss/tokens/person_token/person_token.scss"
import {CSSProperties} from "react";
import {redirect} from "../utils";
import {Person} from "../../../generated/frontend/interfaces/yasm/database";
import {split_avas} from "../../../util/avas";

export interface PersonCardProps {
    person: Person
    style?: CSSProperties
    callback?: () => void
    clickable?: boolean
}

export class PersonToken extends React.Component<PersonCardProps> {
    render() {
        const {latest} = split_avas(this.props.person)
        return <div className={"person_token" + (this.props.clickable ? " person_token--clickable" : "")}
                    style={this.props.style} onClick={() => {
            if (this.props.clickable) {
                if (!this.props.callback)
                    redirect('/admin/gui/people/' + this.props.person.id)
                else
                    this.props.callback()
            }
        }}>
            <img src={latest.repr} className="person_token__img"/>
            <div className="person_token__name">
                {this.props.person.last_name + ' ' + this.props.person.first_name}
            </div>
        </div>
    }
}