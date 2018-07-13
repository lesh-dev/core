import * as React from 'react'
import {Moment} from "moment";
import "../../../scss/dayline/dayline.scss"
import {min} from "rxjs/operators";

export interface Range {
    begin: Moment
    end: Moment
}

export interface DayLineProps {
    range: Range
    selected: Range[]
}

export class DayLine extends React.Component<DayLineProps> {

    blocks() {
        let n = this.props.range.end.diff(this.props.range.begin, 'days') + 1;
        let blocks = [];
        let j = 0;
        for (let i = 0; i < n; i += 1) {
            let cls = "dayline__block ";
            if (j < this.props.selected.length) {
                if (this.props.selected[j].begin.diff(this.props.range.begin, 'days') <= i) {
                    if (this.props.selected[j].end.diff(this.props.range.begin, 'days') >= i) {
                        cls += "dayline__block--selected"
                    } else {
                        j += 1;
                    }
                }
            }
            blocks.push(<div className={cls} key={i}>{
                this.props.range.begin.clone().add(i, 'days').format("DD")
            }</div>)
        }
        return blocks;
    }



    render() {
        return <div className={"dayline"}>
            {this.blocks()}
        </div>
    }
}