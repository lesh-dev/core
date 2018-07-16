import * as React from 'react'
import "../../../scss/course_card/course_card.scss"
import {CSSProperties} from "react";
import {ava_small} from "./utils";
import {Course} from "../../generated/interfaces";

export interface CourseCardProps {
    course: Course
    callback?: () => void
    style?: CSSProperties
}

export class CourseCard extends React.Component<CourseCardProps> {
    render() {
        return <div className="course_card" style={this.props.style} onClick={() => {
            if (this.props.callback)
                this.props.callback()
        }}>
            <div>{this.props.course.course_title}</div>
        </div>
    }
}