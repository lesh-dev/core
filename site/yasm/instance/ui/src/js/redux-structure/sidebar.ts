import { Action, createActions, handleActions, ReducerMap } from 'redux-actions'
import { IconDefinition } from '@fortawesome/fontawesome-svg-core'

export enum SidebarEntryType {
    SuperButton,
    Link,
    Folder,
    ActionButton,
    Spacer,
}

interface SidebarEntryBase {
    type: SidebarEntryType,
    display?: string,
    image?: IconDefinition,
}

export interface SidebarLink extends SidebarEntryBase{
    type: SidebarEntryType.Link,
    url: string,
}

export interface SidebarFolder extends SidebarEntryBase {
    type: SidebarEntryType.Folder,
    opened: boolean,
    children: SidebarEntry,
}

export interface SidebarActionButton extends SidebarEntryBase {
    type: SidebarEntryType.ActionButton,
    action: any,
}

export interface SidebarSuperButton extends SidebarEntryBase {
    type: SidebarEntryType.SuperButton,
}

export interface SidebarSpacer extends SidebarEntryBase {
    type: SidebarEntryType.Spacer,
}

export type SidebarEntry =
    SidebarFolder |
    SidebarLink |
    SidebarActionButton |
    SidebarSpacer |
    SidebarSuperButton

export interface SidebarState {
    collapsed?: boolean,
    entries?: SidebarEntry[],
}

export const sidebarActions = createActions({
    common: {
        sidebar: {
            toggle: () => {}
        }
    }
}) as any


export function getReducer(initialState: SidebarState) {
    return handleActions(
    ({
        common: {
            sidebar: {
                toggle: (state: SidebarState) => ({
                    ...state,
                    collapsed: !state.collapsed,
                })
            },
        }
    }) as ReducerMap<SidebarState, Action<any>>,
    getInitialState(initialState),
)
}

export function getInitialState(initialState: SidebarState): SidebarState {
    return {
        collapsed: false,
        entries: [],
        ...initialState,
    }
}