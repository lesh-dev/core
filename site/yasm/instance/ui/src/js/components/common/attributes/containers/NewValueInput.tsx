import * as React from "react"
import {connect} from "react-redux"
import * as _ from "lodash"
import {Dict} from "awesome-typescript-loader/dist/instance";

import InputPresentation from './InputPresentation'
import { StateShape, Person, InputPresentationProps, InputWrapperProps } from '../types/index'

const inputWrapperMapStateToProps = (state: StateShape) => ({
    editing: state.attribute_table.selectionStatus == 'selected',
    initialValue: 'TODO', // todo: get from state of the first selected cell
    selection: state.attribute_table, // todo
})

const inputWrapperMapDispatchToProps = (dispatch: (action: any)=>void, ownProps: any) => ({
    update: (value: string, selection: StateShape['attribute_table']) =>
        console.log("wrapper input", value, selection) // todo
})

class InputWrapper extends React.Component<InputWrapperProps> {
    render() {
        const props = this.props;
        if(!props.editing) return <span/>;
        return <InputPresentation initialValue={props.initialValue} update={props.update} selection={props.selection}/>
    }
}

export default connect(inputWrapperMapStateToProps, inputWrapperMapDispatchToProps)(InputWrapper)


