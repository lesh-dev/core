import * as React from "react";
import 'react-dates/initialize'
import {School, SchoolList} from "../../generated/interfaces";
import {SchPersonList} from "./sch_person_list";
import {ET} from "../common/EditableText";
import 'react-dates/lib/css/_datepicker.css';
import {DateRange} from "../common/DateRange";
import {Cut} from "../common/Cut";
import {date_2_str, str_2_date} from "../common/utils"
import {Moment} from "moment";
import {Location} from "./Location";
import {school_fill, school_list} from "../../generated/api_connect";
import {Spinner} from "../common/Spinner";
import '../../../scss/school.scss'


export interface SchProps {
    sch: number
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
        school_list({school_id: '' + this.props.sch}).then((value: SchoolList) => {
            if (value.length == 1) {
                school_fill(value.values[0]).then((value: School) => {
                    this.setState({sch_mod: value})
                })
            } else {
                console.log(value);
                console.log("error")
            }
        })
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
        alert('back')
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
        return (this.state) ? <div className="sch">
            <div>
                <div className={"controls"}>
                    <div className={"controls__save"} onClick={() => {
                        this.onSave()
                    }}>🖫
                    </div>
                </div>
            </div>
            <div>
                <div>
                    <ET text={this.state.sch_mod.school_title} callback={(s: string) => {
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
            <Location location_text={this.state.sch_mod.school_location}
                      location_coords={this.state.sch_mod.school_coords}
                      mapclick_callback={(e: any) => {
                          this.onMapClick(e)
                      }}
                      text_edit_callback={(s: string) => {
                          this.onLocationChange(s);
                      }}/>
            <Cut label={"Люди"} content={
                <SchPersonList
                    spl={this.state.sch_mod.person_school_list}
                    callback={(i: number, v: Moment[]) => {
                        this.onPersonDateChange(i, v)
                    }}
                />
            }/>
        </div> : <Spinner/>
    }
}
