import * as React from 'react'
import "../../../scss/person_card/person_card.scss"

export interface PersonCardProps {
    nick: string
    name: string
    img: string
    callback?: () => void
}

export class PersonCard extends React.Component<PersonCardProps> {
    render() {
        return <div className="person_card" onClick={() => {this.props.callback()}}>
            <img src={this.props.img} className="person_card__img"/>
            <div className="person_card__text">
                <div className="person_card__text__name">{this.props.name}</div>
                <div className="person_card__text__nick">@{this.props.nick}</div>
            </div>
        </div>
    }
}