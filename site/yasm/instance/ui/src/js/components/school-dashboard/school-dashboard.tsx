import * as React from "react";
import 'react-dates/initialize'
import {School} from "../../generated/interfaces";
import {SchPersonList} from "./sch_person_list";
import {ET} from "../common/editable_text";
import {DateRangePicker} from 'react-dates';
import 'react-dates/lib/css/_datepicker.css';
import {DateRange} from "../common/DateRange";
import {Cut} from "../common/Cut";
import {date_2_str, str_2_date, str_2_date_format} from "../common/utils"
import {Moment} from "moment";
import {Location} from "./Location";

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
}

export class SchoolDashboard extends React.Component<SchProps, SchState> {
    constructor(props: any) {
        super(props);
        this.state = {
            sch_mod: props.sch,
        }

    }

    onDateChange(value: any) {
        let tmp = this.state.sch_mod;
        if (value.startDate) {
            tmp.school_date_start = date_2_str(value.startDate);
        }
        if (value.endDate) {
            tmp.school_date_end = date_2_str(value.endDate);
        }
        this.setState({
            sch_mod: tmp
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
        let tmp = this.state.sch_mod;
        if (v.startDate) {
            tmp.person_school_list.values[i].frm = date_2_str(v.startDate);
        }
        if (v.endDate) {
            tmp.person_school_list.values[i].tll = date_2_str(v.endDate);
        }
        this.setState({
            sch_mod: tmp
        });
    }

    onBack() {
        this.props.on_back()
    }

    onSave() {
        alert("save")
    }

    onMapClick(event: any) {
        let tmp = this.state.sch_mod;
        tmp.school_coords = event.get("coords").join(", ");
        this.setState({
            sch_mod: tmp
        })
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
                <div>
                    <ET text={this.props.sch.school_title} callback={(s: string) => {
                        this.onTitleChange(s);
                    }}/>
                </div>
            </div>
            <div className="sch__dates">
                <DateRange start={str_2_date(this.state.sch_mod.school_date_start)}
                           end={str_2_date(this.state.sch_mod.school_date_end)}
                           callback={(v: any) => {
                               this.onDateChange(v)
                           }}
                           ph1={"Заезд"}
                           ph2={"Отъезд"}
                           tag={"school_dates"}
                />
            </div>
            <Location location_text={this.props.sch.school_location}
                      location_coords={this.state.sch_mod.school_coords}
                      mapclick_callback={(e: any) => {
                          this.onMapClick(e)
                      }}
                      text_edit_callback={(s: string) => {
                          this.onLocationChange(s);
                      }}/>
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
