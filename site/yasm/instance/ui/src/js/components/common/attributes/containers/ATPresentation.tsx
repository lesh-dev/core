import * as React from "react"
import * as _ from "lodash"

import ATCell from './ATCell'
import CalendarCell from './CalendarCell'
import PersonCell from './PersonCell'
import ColumnCell from './ColumnCell'

import { Column, Config, ATPresentationProps} from '../types/index'

const ATPresentation = ({ config, persons} : ATPresentationProps) =>
    <div>
        <table className="AT_table">
            <tbody>
            <tr className="AT_row">{
                config.map((column, c_index) => <ColumnCell {...column}/>)
            }</tr>
            { persons.map( (p, p_index) =>
                <tr className="AT_row">{
                    config.map((column, c_index) => item(column, p, c_index, p_index, config))
                }</tr>)
            }
            </tbody>
        </table>
    </div>

const item = (column: Column, person_school: number, c_index: number, p_index: number, config: Config) => {
    switch(column.type) {
        case "person":
            return <PersonCell {...{config, person_school, column, c_index, p_index}}/>
        case "calendar":
            return <CalendarCell {...{config, person_school, column, c_index, p_index}}/>
        case "attribute":
        default:
            return <ATCell {...{config, person_school, column, c_index, p_index}}/>
    }
}

export default ATPresentation;