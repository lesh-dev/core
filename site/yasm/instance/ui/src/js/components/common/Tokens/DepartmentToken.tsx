import * as React from 'react'
import "../../../../scss/department_card/department_card.scss"
import {CSSProperties} from "react";
import {Department} from "../../../generated/interfaces";
import {redirect} from "../utils";
import {OnValueClickHandler, Option, OptionValues, ReactSelectProps, SelectValueHandler} from "react-select";

export interface DepartmentCardProps {
    department: Department
    style?: CSSProperties
    clickable?: boolean
    callback?: () => void
}

export class DepartmentToken extends React.Component<DepartmentCardProps> {
    render() {
        return <div className={"department_card" + (this.props.clickable ? " department_card--clickable" : "")}
                    style={this.props.style} onClick={() => {
            if (this.props.clickable) {
                if (!this.props.callback)
                    redirect('/admin/gui/departments/' + this.props.department.department_id)
                else
                    this.props.callback()
            }
        }}>
            <img src={"/static/emblems/departments/" + this.props.department.department_id + ".jpg"}
                 className="department_card__img"/>
            <div className="department_card__title">{this.props.department.department_title}</div>
        </div>
    }
}

export interface DepartmentOptionProps {
    children: any
    className: any
    isDisabled: any
    isFocused: any
    isSelected: any
    onFocus: any
    onSelect: any
    option: Department
}

export class DepartmentOption extends React.Component<DepartmentOptionProps> {
    handleMouseDown(event: any) {
        event.preventDefault();
        event.stopPropagation();
        this.props.onSelect(this.props.option, event);
    }

    handleMouseEnter(event: any) {
        this.props.onFocus(this.props.option, event);
    }

    handleMouseMove(event: any) {
        if (this.props.isFocused) return;
        this.props.onFocus(this.props.option, event);
    }

    render() {
        return <div onMouseEnter={(e: any) => {
            this.handleMouseEnter(e)
        }}
                    onMouseMove={(e: any) => {
                        this.handleMouseMove(e)
                    }}
                    onMouseDown={(e: any) => {
                        this.handleMouseDown(e)
                    }}
        >
            <DepartmentToken department={this.props.option}
                             style={{
                                display: "flex",
                                justifyContent: "left"
                            }}/>
        </div>
    }
}

export interface DepartmentValueProps {
    children: any
    plaseholder: any
    value: Department
}

export class DepartmentValue extends React.Component<DepartmentValueProps> {
    render() {
        return (
            <DepartmentToken department={this.props.value}/>
        );
    }
}


