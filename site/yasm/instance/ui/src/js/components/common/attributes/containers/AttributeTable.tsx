import * as React from "react"
import {connect} from "react-redux"
import * as _ from "lodash"

import ATManager from './ATManager'

const atMapStateToProps = (state: any, ownProps: {school_id: number}) => ({
    school_id: ownProps.school_id,
    person_school_list: state.attribute_table.person_school_list,
})

export default connect(atMapStateToProps)(
    props => <ATManager dispatch={props.dispatch}
                        school_id={props.school_id}
                        person_school_list={props.person_school_list}/>
)