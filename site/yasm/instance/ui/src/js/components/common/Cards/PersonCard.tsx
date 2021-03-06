import * as React from 'react'
import {CSSProperties} from 'react'
import "../../../../scss/cards/person_card/person_card.scss"
import {redirect} from "../utils";
import {Person} from "../../../generated/frontend/interfaces/yasm/database";

export interface PersonCardProps {
    person: Person
    style?: CSSProperties
    callback?: () => void
    clickable?: boolean
    truncated?: boolean
    key?: number
}

export class PersonCard extends React.Component<PersonCardProps> {
    static defaultProps = {
        truncated: false,
    };

    render() {
        const avas = this.props.person.avas
        let ava = null
        if (avas.length > 0)
            ava = avas[0].repr
        return (
            <div className={"person_card" + (this.props.clickable ? " person_card--clickable" : "")}
                 style={this.props.style} onClick={() => {
                if (this.props.clickable) {
                    if (!this.props.callback)
                        redirect('/admin/gui/people/' + this.props.person.id)
                    else
                        this.props.callback()
                }
            }}
                 key={this.props.key || 1}
            >

                <img src={this.props.person.avas.reduce((ava, next) => ava.timestamp > next.timestamp ? ava : next).repr} className="person_card__img"/>
                {!this.props.truncated
                    ? (
                        <div className="person_card__text">
                            <div
                                className="person_card__text__name">{this.props.person.last_name + ' ' + this.props.person.first_name}</div>
                            {this.props.person.nick_name
                                ?
                                <div className="person_card__text__nick">@{this.props.person.nick_name}</div>
                                : null}
                        </div>
                    )
                    : null
                }
            </div>
        )
    }
}
