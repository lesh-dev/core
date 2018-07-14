import * as React from "react";
import 'react-dates/initialize'
import {Department, DepartmentList, School, SchoolList} from "../../generated/interfaces";
import 'react-dates/lib/css/_datepicker.css';
import {getRequest, department_fill, department_list} from "../../generated/api_connect";
import {Spinner} from "../common/Spinner";
import '../../../scss/department/department.scss'


export interface DepartmentDashboardProps {
    department_id: number
}

export interface DepartmentDashboardState {
    department: Department
}

export class DepartmentDashboard extends React.Component<DepartmentDashboardProps, DepartmentDashboardState> {
    constructor(props: any) {
        super(props);
        this.reload()
    }

    reload() {
        department_list({department_id: '' + this.props.department_id}).then((value: DepartmentList) => {
            if (value.length == 1) {
                department_fill(value.values[0]).then((value: Department) => {
                    this.setState({department: value})
                })
            } else {
                console.log(value);
                console.log("error")
            }
        });
    }

    render() {
        return (this.state) ? <div className="department">
            <div className="department__title">
                <img className="department__title__img"
                     src={"/static/emblems/departments/" + this.state.department.department_id + ".jpg"}/>
                <div className="department__title__text">
                    {this.state.department.department_title}
                </div>
            </div>
            <div className="department__additional">
            </div>
        </div> : <Spinner/>
    }
}
