import * as React from "react";
import 'react-dates/initialize'
import {School} from "../generated/interfaces";
import {SchPersonList} from "./sch_person_list";
import {ET} from "./editable_text";
import {DateRangePicker} from 'react-dates';
import 'react-dates/lib/css/_datepicker.css';
import {DateRange} from "./DateRange";
import {Cut} from "./Cut";
import {date_2_str, str_2_date, str_2_date_format} from "./utils"
import {Moment} from "moment";


export interface SchProps {
    sch: School
    on_back: () => void
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
        console.log(dtmp.start);
        console.log(str_2_date(tmp.school_date_start))
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

    onPersonDateChange(i: number, v: any) {
        console.log(v);
        console.log(date_2_str(v.startDate));
        console.log(date_2_str(v.endDate));
        let tmp = this.state.sch_mod;
        if (v.startDate) {
            tmp.person_school_list.values[i].frm = date_2_str(v.startDate);
        }
        if (v.endDate) {
            tmp.person_school_list.values[i].tll = date_2_str(v.endDate);
        }
        console.log(str_2_date_format(tmp.person_school_list.values[i].frm));
        console.log(str_2_date_format(tmp.person_school_list.values[i].tll));
        this.setState({
            sch_mod: tmp
        });
    }

    onBack() {
        console.log("test");
        this.props.on_back()
    }

    onSave() {
        alert("save")
    }

    render() {
        return <div className="sch">
            <div>
                <div className={"controls"}>
                    <div className={"controls__back"} onClick={() => {
                        this.onBack()
                    }}>🡄
                    </div>
                    <div className={"controls__save"} onClick={() => {
                        this.onSave()
                    }}>🖫
                    </div>
                </div>
            </div>
            <div>
                <ET text={this.props.sch.school_title} callback={(s: string) => {
                    this.onTitleChange(s);
                }}/>
            </div>
            <div className="sch__dates">
                <DateRange start={str_2_date(this.state.sch_mod.school_date_start)}
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
                <ET text={this.props.sch.school_location ? this.props.sch.school_location : "Место не указано"} callback={(s: string) => {
                    this.onLocationChange(s);
                }}/>
            </div>
            <Cut label={"Люди"} content={
                <SchPersonList
                    spl={this.props.sch.person_school_list}
                    callback={(i: number, v: Moment[]) => {
                        this.onPersonDateChange(i, v)
                    }}
                />
            }/>
        </div>
    }
}
