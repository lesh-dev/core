import * as React from "react";
import 'react-dates/initialize'
import {School} from "../generated/interfaces";
import {PersSchList} from "./pers_sch_list";
import {ET} from "./editable_text";
import {DateRangePicker} from 'react-dates';
import 'react-dates/lib/css/_datepicker.css';
import {DateRange} from "./DateRange";


export interface SchProps {
    sch: School
}

export interface DateState {
    focus: any
    start: any
    end: any
}

export interface SchState {
    sch_mod: School
    dates: DateState
}

export class Sch extends React.Component<SchProps, SchState> {
    constructor(props: any) {
        super(props);
        this.state = {
            sch_mod: props.sch,
            dates: {
                focus: null,
                start: null,
                end: null
            }
        }

    }

    onDateChange(value: any) {
        let tmp = this.state.sch_mod;
        let dtmp = this.state.dates;
        if (value.startDate) {
            tmp.school_date_start = "" + value.startDate.year() + "." + value.startDate.month() + "." + value.startDate.day();
        }

        if (value.endDate) {
            tmp.school_date_end = "" + value.endDate.year() + "." + value.endDate.month() + "." + value.endDate.day();
        }
        dtmp.end = value.endDate;
        dtmp.start = value.startDate;
        this.setState({
            sch_mod: tmp,
            dates: dtmp
        });
    }

    render() {
        return <div className="sch">
            <div>
                <ET text={this.props.sch.school_title} callback={() => {
                }}/>
            </div>
            <div className="sch__dates">
                <DateRange start={this.state.dates.start} end={this.state.dates.end} callback={(v: any) => {this.onDateChange(v)}}/>
            </div>
            <PersSchList psl={this.props.sch.person_school_list}/>
        </div>
    }
}