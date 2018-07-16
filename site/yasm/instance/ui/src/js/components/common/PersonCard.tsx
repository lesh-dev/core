import * as React from 'react'
import "../../../scss/person_card/person_card.scss"
import {CSSProperties} from "react";
import {ava_small, redirect} from "./utils";
import {Person} from "../../generated/interfaces";
import Async from "react-promise"

export interface PersonCardProps {
    person: Person
    style?: CSSProperties
    clickable?: boolean
}

export class PersonCard extends React.Component<PersonCardProps> {
    render() {
        return <div className="person_card" style={this.props.style} onClick={() => {
            if (this.props.clickable)
                redirect('/admin/gui/people/' + this.props.person.person_id)
        }}>
            <Async promise={ava_small(this.props.person)} then={val => {
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