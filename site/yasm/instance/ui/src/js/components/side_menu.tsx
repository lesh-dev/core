import * as React from "react";

export interface EntryProps {
    label: string,
    url: string,
    entries: EntryProps[]
}

export interface SideMenuProps {
    entries: EntryProps[]
}

class Entry extends React.Component<EntryProps> {
    render() {
        return <div></div>
    }
}

export class SideMenu extends React.Component<SideMenuProps, undefined> {
    render() {
        return <div className="side_menu">
        </div>
    }
}