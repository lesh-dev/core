import * as React from "react";

export interface Entry {
    label: string,
    url: string,
    entries: Entry[]
}

export interface SideMenuProps {
    entries: Entry[]
}

class Entry extends React.Component<> {

}

export class SideMenu extends React.Component<SideMenuProps, undefined> {
    render() {
        return <div className="side_menu">

        </div>
    }
}