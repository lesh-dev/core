const AT_MOUSE_DOWN = 'AT_MOUSE_DOWN';
const AT_MOUSE_UP = 'AT_MOUSE_UP';
const AT_MOUSE_OVER = 'AT_MOUSE_OVER';
const AT_CLICK = 'AT_CLICK';
const LOADED_ATTRIBUTES = "LOADED_ATTRIBUTES";

import { Column } from '../types/index';

export const atMouseDown = (column: Column, person_school: number, c_index: number, p_index: number) => ({
    type: AT_MOUSE_DOWN,
    column,
    person_school,
    c_index,
    p_index,
})
export const atMouseUp = (column: Column, person_school: number, c_index: number, p_index: number) => ({
    type: AT_MOUSE_UP,
    column,
    person_school,
    c_index,
    p_index,
})
export const atMouseOver = (column: Column, person_school: number, c_index: number, p_index: number) => ({
    type: AT_MOUSE_OVER,
    column,
    person_school,
    c_index,
    p_index,
})
export const atClick = (column: Column, person_school: number, c_index: number, p_index: number) => ({
    type: AT_CLICK,
    column,
    person_school,
    c_index,
    p_index,
})

export const loadedAttributes = (entities: any, person_school_list: any) => ({
    type: LOADED_ATTRIBUTES,
    entities,
    person_school_list,
})

