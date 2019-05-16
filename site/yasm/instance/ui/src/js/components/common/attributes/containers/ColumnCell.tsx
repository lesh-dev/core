import * as React from "react"
import {connect} from "react-redux"
import * as _ from "lodash"
import {Dict} from "awesome-typescript-loader/dist/instance";

import { atMouseDown, atMouseUp, atMouseOver, atClick } from '../actions/AttributesActions'
import NewValueInput from './NewValueInput'

import { Person, StateShape, ATCOwnProps, Column, Config } from '../types/index'

const calendarMapStateToProps = (state: StateShape, ownProps: Column) => ({
    value: ownProps.field
})


export default connect(calendarMapStateToProps)((props: {value: string}) =>
    <td>
    <div className={ "AT_cell AT_header" }>
        {props.value}
    </div>
    </td>
)

