import * as React from 'react'
import {AnchorDirectionShape, DateRangePicker} from 'react-dates';
import {Moment} from "moment";

export interface DateRangeProps {
    ph1: string
    ph2: string
    tag: string
    start: Moment
    end: Moment
    callback: (vals: any) => void
    onFocus?: (focus: any) => void
    anchorDirection?: AnchorDirectionShape
}

export interface DateRangeState {
    focus: any
}

export class DateRange extends React.Component<DateRangeProps, DateRangeState> {
    constructor(props: any) {
        super(props);
        this.state = {
            focus: null
        }
    }
    date_focus (focus: any) {
        this.setState({focus: focus});
        if (this.props.onFocus)
        this.props.onFocus(focus)
    }

    render() {
        return <DateRangePicker
                    startDate={this.props.start}
                    startDateId={this.props.tag + "_start"}
                    startDatePlaceholderText={this.props.ph1}
                    endDate={this.props.end}
                    endDateId={this.props.tag + "_end"}
                    endDatePlaceholderText={this.props.ph2}
                    onDatesChange={(v: any) => {this.props.callback(v)}}
                    onFocusChange={focusedInput => {this.date_focus(focusedInput)}}
                    focusedInput={this.state.focus}
                    displayFormat={"DD MMM YY"}
                    block={true}
                    showClearDates={true}
                    reopenPickerOnClearDates={true}
                    firstDayOfWeek={1}
                    regular={true}
                    anchorDirection={this.props.anchorDirection}
                />
    }
}