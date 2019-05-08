import * as React from "react"
import {connect} from "react-redux"
import * as _ from "lodash"
import {Dict} from "awesome-typescript-loader/dist/instance";

import { atMouseDown, atMouseUp, atMouseOver, atClick } from '../actions/AttributesActions'
import NewValueInput from './NewValueInput'

import { Person, StateShape, ATCOwnProps, Column, Config } from '../types/index'

function isSelected(state: StateShape, p_index: number, c_index: number) {
    if(!state || !state.attribute_table) return false;
    const at = state.attribute_table;
    const p = at.selectionStartP <= p_index && p_index <= at.selectionEndP;
    const c = at.selectionStartC <= c_index && c_index <= at.selectionEndC;
    return p && c;
}

function isEndOfSelection(state: StateShape, p_index: number, c_index: number) {
    if(!state || !state.attribute_table) return false;
    const at = state.attribute_table;
    return at.selectionEndP == p_index && at.selectionEndC == c_index;
}

const mapStateToProps = (state: StateShape, ownProps: ATCOwnProps) => ({
    value: (state && state.entities && state.entities.person_schools) ?
        (state.entities.persons
            [state.entities.person_schools[ownProps.person_school].person] as any)
            [ownProps.column.field]
        : "",
    isSelected: isSelected(state, ownProps.p_index, ownProps.c_index),
    isEndOfSelection: isEndOfSelection(state, ownProps.p_index, ownProps.c_index),
})



const atcMapDispatchToProps = (dispatch: (action: any) => void, ownProps: ATCOwnProps) => ({
    onClick: () => {
        dispatch(atClick(ownProps.column, ownProps.person_school, ownProps.c_index, ownProps.p_index))
    },
    onMouseDown: () => {
        dispatch(atMouseDown(ownProps.column, ownProps.person_school, ownProps.c_index, ownProps.p_index))
    },
    onMouseOver: () => {
        // fixme? need to know if selection started? Or is this a problem of reducer?
        dispatch(atMouseOver(ownProps.column, ownProps.person_school, ownProps.c_index, ownProps.p_index))
    },
    onMouseUp: () => {
        dispatch(atMouseUp(ownProps.column, ownProps.person_school, ownProps.c_index, ownProps.p_index))
    },
})

export default connect(mapStateToProps, atcMapDispatchToProps)(props =>
    <td>
    <div onMouseDown={props.onMouseDown}
        onMouseUp={props.onMouseUp}
        onMouseOver={props.onMouseOver}
        onClick={props.onClick}
        className={ "AT_cell" + (props.isSelected ? " attribute-table__cell_selected" : "") + (props.isEndOfSelection ? " attribute-table__cell_end-of-selection" : "") }>
        {props.value}
        { props.isEndOfSelection && <NewValueInput/> }
        </div>
    </td>
)

