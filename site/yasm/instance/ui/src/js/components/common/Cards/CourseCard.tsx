import * as React from 'react'
import "../../../../scss/cards/course_card/course_card.scss"
import {CSSProperties} from "react";
import {Course} from "../../../generated/frontend/interfaces/yasm/database";

export interface CourseCardProps {
    course: Course
    clickable?: boolean
    callback?: () => void
    style?: CSSProperties
}

export class CourseCard extends React.Component<CourseCardProps> {
    render() {
        return <div className="course_card" style={this.props.style} onClick={() => {
            if (this.props.callback)
                this.props.callback()
        }}>
            <div>{this.props.course.title}</div>
        </div>
    }
}