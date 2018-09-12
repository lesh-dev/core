import * as React from 'react'
import "../../../../scss/tokens/person_token/person_token.scss"
import {CSSProperties} from "react";
import {ava, redirect} from "../utils";
import {Person} from "../../../generated/interfaces";
import Async from "react-promise"

export interface PersonCardProps {
    person: Person
    style?: CSSProperties
    callback?: () => void
    clickable?: boolean
}

export class PersonToken extends React.Component<PersonCardProps> {
    render() {
        return <div className={"person_token" + (this.props.clickable ? " person_token--clickable" : "")}
                    style={this.props.style} onClick={() => {
            if (this.props.clickable) {
                if (!this.props.callback)
                    redirect('/admin/gui/people/' + this.props.person.person_id)
                else
                    this.props.callback()
            }
        }}>
            <Async promise={ava(this.props.person)} then={val => {
                return <img src={val} className="person_token__img"/>
            }}/>
            <div className="person_token__name">
                {this.props.person.last_name + ' ' + this.props.person.first_name}
            </div>
        </div>
    }
}