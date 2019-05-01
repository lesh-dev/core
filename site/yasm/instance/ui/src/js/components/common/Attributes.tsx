import * as React from "react"
import {connect, Provider, Store} from "react-redux"
import {applyMiddleware, combineReducers, createStore} from "redux"
import thunkMiddleware from 'redux-thunk'
import { createLogger } from 'redux-logger'
import { composeWithDevTools } from 'redux-devtools-extension'
import * as nm from "normalizr"
import { Lens } from "./Search"
import {HighlightTitle} from "./Snippet";
import * as _ from "lodash"
import {Dict} from "awesome-typescript-loader/dist/instance";




const getAttributes = (school_id: number) => fetch(`
    /postgrest/person_school?
    select=person_school_id,person(*),person_attributes(*)
    &school_id=eq.${school_id}
    `.replace(/ +/g, ''))
    .then(resp => resp.json())
    .then(normalizeAttributes)

type Person = { person_id: number, first_name: string, last_name: string }
type Attr = { person_school_id: number, field: string, value: string }
type AttributeResponseItem = { person_school_id: number, person: Person, person_attributes: Attr[] }

function normalizeAttributes(resp: AttributeResponseItem[]) {
    function reshapeAttrs(attrs: Attr[]) {
        return Object.assign({}, ...attrs.map(a => ({ [a.field]: a.value })) );
    }
    function reshapeItem(item: AttributeResponseItem) {
        const {person_attributes, ...rest} = item;
        return {person_attributes: reshapeAttrs(person_attributes), ...rest};
    }
    const reshaped = resp.map(reshapeItem);

    const person = new nm.schema.Entity('persons', {}, {idAttribute: 'person_id'});
    const person_school = new nm.schema.Entity('person_schools', {person}, {idAttribute: 'person_school_id'});
    const {entities, result} = nm.normalize(reshaped, [person_school]);
    return {entities, result};
}








type StateShape = {
    entities: {
        persons: Dict<Person>
        person_schools: Dict<{person_school_id: number, person_attributes: Dict<string>}>
    }
    attribute_table: {
        person_school_list: number[],
        selectionStatus: 'started' | 'intermediate' | 'selected',
        selectionType: string,
        selectionStartP: number,
        selectionStartC: number,
        selectionEndP: number,
        selectionEndC: number,
    }
}

type Column = { type: string, field: string }
type Config = Column[]

type ATPresentationProps = { config: Config, persons: number[] }

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
        case "dbcolumn":
        case "attribute":
        default:
            return <ATCell {...{config, person_school, column, c_index, p_index}}/>
    }
}


type ATCOwnProps = { person_school: number, column: Column, p_index: number, c_index: number, config: Config }

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

const atcMapStateToProps = (state: StateShape, ownProps: ATCOwnProps) => ({
    value: (state && state.entities && state.entities.person_schools) ?
        state.entities.person_schools[ownProps.person_school].person_attributes[ownProps.column.field]
        : "",
    isSelected: isSelected(state, ownProps.p_index, ownProps.c_index),
    isEndOfSelection: isEndOfSelection(state, ownProps.p_index, ownProps.c_index),
})

const AT_MOUSE_DOWN = 'AT_MOUSE_DOWN';
const AT_MOUSE_UP = 'AT_MOUSE_UP';
const AT_MOUSE_OVER = 'AT_MOUSE_OVER';
const AT_CLICK = 'AT_CLICK';

const atMouseDown = (column: Column, person_school: number, c_index: number, p_index: number) => ({
    type: AT_MOUSE_DOWN,
    column,
    person_school,
    c_index,
    p_index,
})
const atMouseUp = (column: Column, person_school: number, c_index: number, p_index: number) => ({
    type: AT_MOUSE_UP,
    column,
    person_school,
    c_index,
    p_index,
})
const atMouseOver = (column: Column, person_school: number, c_index: number, p_index: number) => ({
    type: AT_MOUSE_OVER,
    column,
    person_school,
    c_index,
    p_index,
})
const atClick = (column: Column, person_school: number, c_index: number, p_index: number) => ({
    type: AT_CLICK,
    column,
    person_school,
    c_index,
    p_index,
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

const ATCell = connect(atcMapStateToProps, atcMapDispatchToProps)(props =>
    <td onMouseDown={props.onMouseDown}
        onMouseUp={props.onMouseUp}
        onMouseOver={props.onMouseOver}
        onClick={props.onClick}
        className={ (props.isSelected ? "attribute-table__cell_selected" : "") + " " + (props.isEndOfSelection ? "attribute-table__cell_end-of-selection" : "") }>
        {props.value}
        { props.isEndOfSelection && <NewValueInput/> }
    </td>
)






const LOADED_ATTRIBUTES = "LOADED_ATTRIBUTES";
const loadedAttributes = (entities: any, person_school_list: any) => ({
    type: LOADED_ATTRIBUTES,
    entities,
    person_school_list,
})

const exampleConfig: Config = [{type: "attribute", field: "example"}, {type: "attribute", field: "play"}]

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




const atMapStateToProps = (state: any, ownProps: {school_id: number}) => ({
    school_id: ownProps.school_id,
    person_school_list: state.attribute_table.person_school_list,
})

const AttributeTable = connect(atMapStateToProps)(
    props => <ATManager dispatch={props.dispatch}
                        school_id={props.school_id}
                        person_school_list={props.person_school_list}/>
)





type InputPresentationProps = {
    initialValue: string,
    selection: StateShape['attribute_table'], // todo
    update(value: string, selection: StateShape['attribute_table']): void
}
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
type InputWrapperProps = InputPresentationProps & {
    editing: boolean,
}
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
const NewValueInput = connect(inputWrapperMapStateToProps, inputWrapperMapDispatchToProps)(InputWrapper)





const reducer = (state: StateShape, action: any) => {
    let at = state.attribute_table;
    switch(action.type) {
        case LOADED_ATTRIBUTES:
            const {entities, person_school_list} = action;
            return _.merge({}, state, {entities, attribute_table: {person_school_list}});
        // Started(Td1) --[Click(Td2)]--> Started(Td2)
        // Started(Td1) --[MouseDown(Td1)]--> Intermediate(Td1, Td1) --[MouseOver(Td2)]--> Intermediate(Td1,Td2)
        //   --[MouseUp(Td3)]--> Selected(Td1,Td3)
        // Started(Td1) --[Click(Td1)]--> Selected(Td1,Td1)
        // Словами: чтобы редактировать ячейку, надо дважды кликнуть на неё.
        // Чтобы выделить несколько, надо кликнуть на начальную, потом мышкой выделить от неё до другого угла.
        case AT_CLICK:
            // double click on same cell -- will be handled by mouse up
            if (action.c_index == at.selectionStartC
                && action.p_index == at.selectionStartP
                && at.selectionStatus == 'started') return state;
            // ignore click in the end of selection
            if (at.selectionStatus == 'intermediate') return state;
            // click on new cell
            return _.merge({}, state, {
                attribute_table: {
                    // selectionStatus: 'started',
                    selectionStartP: action.p_index,
                    selectionStartC: action.c_index,
                }
            });

        case AT_MOUSE_DOWN:
            // ignore mouse down on new cell -- will be handled by click
            if (action.c_index != at.selectionStartC || action.p_index != at.selectionStartP) return state;
            return _.merge({}, state, {
                attribute_table: {
                    selectionStatus: 'intermediate',
                    selectionEndP: action.p_index,
                    selectionEndC: action.c_index,
                }
            });
        case AT_MOUSE_OVER:
            // todo
            return state;
        case AT_MOUSE_UP:
            return _.merge({}, state, {
                attribute_table: {
                    selectionStatus: 'selected',
                    selectionEndP: action.p_index,
                    selectionEndC: action.c_index,
                }
            });
        default:
            return state;
    }
}

const initialState: StateShape = {
    entities: {
        persons: {},
        person_schools: {} as Dict<{person_school_id: number, person: number, person_attributes: Dict<string>}>
    },
    attribute_table: {
        person_school_list: [] as number[],
        selectionStatus: "started", // started | intermediate | selected
        selectionType: "attribute",
        selectionStartP: -1,
        selectionStartC: -1,
        selectionEndP: -1,
        selectionEndC: -1,
    }
}

let enhancer: any;
/// #if ENV === "development"
enhancer = composeWithDevTools( applyMiddleware(thunkMiddleware, createLogger()) );
/// #else
enhancer = null;
/// #endif
const makeStore = () => createStore(reducer, initialState, enhancer);

export const ATExample = () => <Provider store={makeStore()}><AttributeTable school_id={20}/></Provider>
