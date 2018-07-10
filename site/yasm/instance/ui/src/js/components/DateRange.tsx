import * as React from 'react'
import {DateRangePicker} from 'react-dates';
import {Moment} from "moment";

export interface DateRangeProps {
    start: Moment
    end: Moment
    callback: (vals: Moment[]) => void
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
        this.setState({focus: focus})
    }

    render() {
        return <DateRangePicker
                    startDate={this.props.start}
                    startDateId="date_start"
                    startDatePlaceholderText="Заезд"
                    endDate={this.props.end}
                    endDateId="date_end"
                    endDatePlaceholderText="Отъезд"
                    onDatesChange={(v: any) => {this.props.callback(v)}}
                    onFocusChange={focusedInput => {this.date_focus(focusedInput)}}
                    focusedInput={this.state.focus}
                    displayFormat={"YY MMM DD"}
                    block={true}
                    showClearDates={true}
                    reopenPickerOnClearDates={true}
                />
    }
}