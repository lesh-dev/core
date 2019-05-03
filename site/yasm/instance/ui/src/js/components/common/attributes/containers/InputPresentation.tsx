import * as React from "react"
import * as _ from "lodash"
import {Dict} from "awesome-typescript-loader/dist/instance";

import { StateShape, Person, InputPresentationProps } from '../types/index'

class InputPresentation extends React.Component<InputPresentationProps, { value: string }> {
    constructor(props: InputPresentationProps) {
        super(props);
        this.state = {
            value: props.initialValue,
        };
    }
    render() {
        return <form onSubmit={(e) => {e.preventDefault(); this.props.update(this.state.value, this.props.selection)}}>
            <input type="text" value={this.state.value}
                   onChange={e => this.setState({ value: e.target.value })}/>
            <button type="submit">set</button>
        </form>
    }
    // fixme componentDidMount?
}

export default InputPresentation;