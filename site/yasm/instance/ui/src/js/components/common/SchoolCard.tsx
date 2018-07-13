import * as React from 'react'
import "../../../scss/school_card/school_card.scss"
import {CSSProperties} from "react";

export interface SchoolCardProps {
    title: string
    dates: string
    place: string
    emblem: string
    callback?: () => void
    style?: CSSProperties
}

export class SchoolCard extends React.Component<SchoolCardProps> {
    render() {
        return <div className="school_card" style={this.props.style} onClick={() => {this.props.callback()}}>
            <img src={this.props.emblem} className="school_card__img"/>
            <div className="school_card__title">{this.props.title}</div>
            <div className="school_card__meta">
                <div className="school_card__meta__name">{this.props.dates}</div>
                <div className="school_card__meta__nick">{this.props.place}</div>
            </div>
        </div>
    }
}