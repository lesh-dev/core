import * as React from "react";
import {Input} from "./Input";


export interface ETProps {
    text: string
    callback: (s: string) => void
    className?: string
}

export interface ETState {
    status: string
    first_text: string
    current_text: string
}


export class ET extends React.Component<ETProps, ETState> {
    constructor(props: Readonly<ETProps>) {
        super(props);
        this.state = {
            status: "def",
            first_text: this.props.text,
            current_text: this.props.text
        }
    }

    edit(value: string) {
        if (value != this.state.first_text) {
            this.setState({status: "mod"})
        } else {
            this.setState({status: "def"})
        }
        this.setState({current_text: value});
        this.props.callback(value)
    }

    render() {
        return <Input className={this.props.className} placeholder={this.state.current_text} callback={(v: any) => this.edit(v)}/>
    }
}