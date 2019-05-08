import * as React from "react"
import * as _ from "lodash"

import ATCell from './ATCell'
import CalendarCell from './CalendarCell'

import { Column, Config, ATPresentationProps} from '../types/index'

const ATPresentation = ({ config, persons} : ATPresentationProps) =>
    <div>
        <table>
            <tbody>
            { persons.map( (p, p_index) =>
                <tr>{
                    config.map((column, c_index) => item(column, p, c_index, p_index, config))
                }</tr>)
            }
            </tbody>
        </table>
    </div>

const item = (column: Column, person_school: number, c_index: number, p_index: number, config: Config) => {
    switch(column.type) {
        case "calendar":
            return <CalendarCell {...{config, person_school, column, c_index, p_index}}/>
        case "dbcolumn":
        case "attribute":
        default:
            return <ATCell {...{config, person_school, column, c_index, p_index}}/>
    }
}

export default ATPresentation;