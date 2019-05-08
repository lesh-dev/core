import * as React from "react"
import * as _ from "lodash"
import * as nm from "normalizr"

import { Person, Attr, AttributeResponseItem} from '../types/index'

function normalizeAttributes(resp: AttributeResponseItem[]) {
    function reshapeAttrs(attrs: Attr[]) {
        return Object.assign({}, ...attrs.map(a => ({ [a.field]: a.value })) );
    }
    function reshapeCalendar(attrs: any[]) { // FIXME
        return Object.assign({}, ...attrs.map(a => ({ [a.data]: a.status })) );
    }
    function reshapeItem(item: AttributeResponseItem) {
        const {person_attributes, calendar, ...rest} = item;
        return {person_attributes: reshapeAttrs(person_attributes), calendar: reshapeCalendar(calendar), ...rest};
    }
    const reshaped = resp.map(reshapeItem);

    const person = new nm.schema.Entity('persons', {}, {idAttribute: 'person_id'});
    const person_school = new nm.schema.Entity('person_schools', {person}, {idAttribute: 'person_school_id'});
    const {entities, result} = nm.normalize(reshaped, [person_school]);
    return {entities, result};
}


const getAttributes = (school_id: number) => fetch(`
    /postgrest/person_school?
    select=person_school_id,person(*),person_attributes(*),calendar(*)
    &school_id=eq.${school_id}
    `.replace(/ +/g, ''))
    .then(resp => resp.json())
    .then(normalizeAttributes)

import ATPresentation from './ATPresentation'

import { loadedAttributes } from '../actions/AttributesActions'

type Column = { type: string, field: string }
type Config = Column[]

const exampleConfig: Config = [
    {type: "person", field: "first_name"},
    {type: "person", field: "last_name"},
    {type: "attribute", field: "example"},
    {type: "attribute", field: "play"},
    {type: "calendar", field: "2019-07-27"}
]

type Dispatch = (action: any) => void;

class ATManager extends React.Component<{dispatch: Dispatch, school_id: number, person_school_list: number[]}> {
    render() {
        return <ATPresentation config={exampleConfig} persons={this.props.person_school_list}/>
    }
    componentDidMount() {
        getAttributes(this.props.school_id)
            .then(val => this.props.dispatch(loadedAttributes(val.entities, val.result))  )
        // todo: run regular updates
    }
    componentWillUnmount() {
        // todo: stop regular updates
    }
}


export default ATManager;