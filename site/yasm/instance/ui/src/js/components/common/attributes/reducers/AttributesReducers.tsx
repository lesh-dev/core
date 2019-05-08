import * as React from "react"
import * as _ from "lodash"
import {Dict} from "awesome-typescript-loader/dist/instance";

const AT_MOUSE_DOWN = 'AT_MOUSE_DOWN';
const AT_MOUSE_UP = 'AT_MOUSE_UP';
const AT_MOUSE_OVER = 'AT_MOUSE_OVER';
const AT_CLICK = 'AT_CLICK';
const LOADED_ATTRIBUTES = "LOADED_ATTRIBUTES";

import { StateShape, Person } from '../types/index'

export const initialState: StateShape = {
    entities: {
        persons: {},
        person_schools: {} as Dict<{person_school_id: number, person: number, person_attributes: Dict<string>, calendar: Dict<string>}>
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

export const reducer = (state: StateShape, action: any) => {
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

