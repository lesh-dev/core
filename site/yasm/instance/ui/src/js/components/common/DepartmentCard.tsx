import * as React from 'react'
import "../../../scss/department_card/department_card.scss"
import {CSSProperties} from "react";

export interface DepartmentCardProps {
    title: string
    emblem: string
    callback: () => void
    style?: CSSProperties
}

export class DepartmentCard extends React.Component<DepartmentCardProps> {
    render() {
        return <div className="department_card" style={this.props.style} onClick={() => {this.props.callback()}}>
            <img src={this.props.emblem} className="department_card__img"/>
            <div className="department_card__title">{this.props.title}</div>
        </div>
    }
}