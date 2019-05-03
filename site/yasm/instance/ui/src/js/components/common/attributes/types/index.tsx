import {Dict} from "awesome-typescript-loader/dist/instance";

export type StateShape = {
    entities: {
        persons: Dict<Person>
        person_schools: Dict<{person_school_id: number, person_attributes: Dict<string>, calendar: Dict<string>}>
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


export type ATCOwnProps = { person_school: number, column: Column, p_index: number, c_index: number, config: Config }
export type Person = { person_id: number, first_name: string, last_name: string }
export type Column = { type: string, field: string }
export type Config = Column[]

export type Attr = { person_school_id: number, field: string, value: string }
export type AttributeResponseItem = { person_school_id: number, person: Person, person_attributes: Attr[], calendar: Attr[] }

export type ATPresentationProps = { config: Config, persons: number[] }

export type InputPresentationProps = {
    initialValue: string,
    selection: StateShape['attribute_table'], // todo
    update(value: string, selection: StateShape['attribute_table']): void
}

export type InputWrapperProps = InputPresentationProps & {
    editing: boolean,
}


