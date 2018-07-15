import * as React from 'react'
import "../../../scss/person_card/person_card.scss"
import {CSSProperties} from "react";
import {vk_ava_small} from "./utils";
import {Person} from "../../generated/interfaces";

export interface PersonCardProps {
    person: Person
    callback?: () => void
    style?: CSSProperties
}

export class PersonCard extends React.Component<PersonCardProps> {
    render() {
        return <div className="person_card" style={this.props.style} onClick={() => {
            this.props.callback()
        }}>
            <img src={vk_ava_small(this.props.person)} className="person_card__img"/>
            <div className="person_card__text">
                <div className="person_card__text__name">{this.props.person.last_name + ' ' + this.props.person.first_name}</div>
                {this.props.person.nick_name ? <div className="person_card__text__nick">@{this.props.person.nick_name}</div> : null}
            </div>
        </div>
    }
}