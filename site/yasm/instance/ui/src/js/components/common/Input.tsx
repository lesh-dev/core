import * as React from "react";
import "../../../scss/input/input.scss"

export interface InputState {
    focus: boolean
    value: string
}

export interface InputProps {
    className?: string,
    name?: string,
    placeholder?: string
    callback?: (v: any) => void
}

export class Input extends React.Component<InputProps, InputState> {
    constructor(props: any) {
        super(props);
        this.state = {
            focus: false,
            value: this.props.placeholder
        };
    }

    handleBlur(event: any) {
        event.target.value = ""
        this.setState({focus: false});
        if (this.state.value != "") {
            if (this.props.callback) {
                this.props.callback(this.state.value);
            }
        }
    }

    handleChange(event: any) {
        let value = event.target.value;

        let stateObj = {
            value: value,
            focus: false
        };

        if (value != "") {
            stateObj.focus = true;
        }

        this.setState(stateObj);
    }

    handleFocus() {
        this.setState({focus: true});
    }

    render() {
        let className = "input-container";

        if (this.props.className) {
            className += this.props.className;
        }

        let labelClass = "";
        if (this.state.focus) {
            labelClass = "focused";
        }

        return (
            <div className={className}
                 onFocus={this.handleFocus.bind(this)}
                 onBlur={this.handleBlur.bind(this)}>
                <label className={labelClass}>
                    {this.props.placeholder}
                </label>
                <input name={this.props.name}
                       onChange={this.handleChange.bind(this)}/>
            </div>);
    }
}
