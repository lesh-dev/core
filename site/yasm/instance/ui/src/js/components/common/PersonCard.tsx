import * as React from 'react'
import "../../../scss/person_card/person_card.scss"
import {CSSProperties} from "react";

export interface PersonCardProps {
    nick: string
    name: string
    img: string
    callback?: () => void
    style?: CSSProperties
}

export class PersonCard extends React.Component<PersonCardProps> {
    render() {
        return <div className="person_card" style={this.props.style} onClick={() => {
            this.props.callback()
        }}>
            <img src={this.props.img} className="person_card__img"/>
            <div className="person_card__text">
                <div className="person_card__text__name">{this.props.name}</div>
                {this.props.nick ? <div className="person_card__text__nick">@{this.props.nick}</div> : null}
            </div>
        </div>
    }
}