import * as React from 'react'
import "../../../../scss/cards/person_card/person_card.scss"
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

export class PersonCard extends React.Component<PersonCardProps> {
    render() {
        return <div className={"person_card" + (this.props.clickable ? " person_card--clickable" : "")}
                    style={this.props.style} onClick={() => {
            if (this.props.clickable) {
                if (!this.props.callback)
                    redirect('/admin/gui/people/' + this.props.person.person_id)
                else
                    this.props.callback()
            }
        }}>
            <Async promise={ava(this.props.person)} then={(val: string) => {
                return <img src={val} className="person_card__img"/>
            }}/>
            <div className="person_card__text">
                <div
                    className="person_card__text__name">{this.props.person.last_name + ' ' + this.props.person.first_name}</div>
                {this.props.person.nick_name ?
                    <div className="person_card__text__nick">@{this.props.person.nick_name}</div> : null}
            </div>
        </div>
    }
}