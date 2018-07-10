import * as React from "react";
import 'react-dates/initialize'
import {School} from "../generated/interfaces";
import {SchPersonList} from "./sch_person_list";
import {ET} from "./editable_text";
import {DateRangePicker} from 'react-dates';
import 'react-dates/lib/css/_datepicker.css';
import {DateRange} from "./DateRange";
import {Cut} from "./Cut";
import {date_2_str, str_2_date} from "./utils"
import {Moment} from "moment";


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
                start: str_2_date(props.sch.school_date_start),
                end: str_2_date(props.sch.school_date_end)
            }
        }

    }

    onDateChange(value: any) {
        console.log(value);
        let tmp = this.state.sch_mod;
        let dtmp = this.state.dates;
        if (value.startDate) {
            tmp.school_date_start = date_2_str(value.startDate);
        }

        if (value.endDate) {
            tmp.school_date_end = date_2_str(value.endDate);
        }
        dtmp.end = value.endDate;
        dtmp.start = value.startDate;
        this.setState({
            sch_mod: tmp,
            dates: dtmp
        });
    }

    onTitleChange(s: string) {
        let tmp = this.state.sch_mod;
        tmp.school_title = s;
        this.setState({sch_mod: tmp});
    }

    onLocationChange(s: string) {
        let tmp = this.state.sch_mod;
        tmp.school_location = s;
        this.setState({sch_mod: tmp});
    }

    render() {
        return <div className="sch">
            <div>
                <ET text={this.props.sch.school_title} callback={(s: string) => {
                    this.onTitleChange(s);
                }}/>
            </div>
            <div className="sch__dates">
                <DateRange start={this.state.dates.start}
                           end={this.state.dates.end}
                           callback={(v: any) => {
                    this.onDateChange(v)
                }}
                           ph1={"Заезд"}
                           ph2={"Отъезд"}
                           tag={"school_dates"}
                />
            </div>
            <div>
                <ET text={this.props.sch.school_location} callback={(s: string) => {
                    this.onLocationChange(s);
                }}/>
            </div>
            <Cut label={"Люди"} content={
                new SchPersonList({spl: this.props.sch.person_school_list})
            }/>
        </div>
    }
}
