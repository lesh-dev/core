import * as React from 'react'
import {Cut} from "./Cut";
import {Link} from "react-router-dom";
import "../../../scss/side_menu/side_menu.scss"

export interface SideMenuEntryProps {
    url?: string
    label: string
    subentries?: SideMenuEntryProps[]
}

export interface SideMenuProps {
    entries: SideMenuEntryProps[]
}

class SideMenuEntry extends React.Component<SideMenuEntryProps> {
    render(): any {
        if (! this.props.url) {
            return <div className="side_menu__entry"><Cut label={this.props.label} content={<SideMenu entries={this.props.subentries}/>}/></div>
        } else {
            return <div className="side_menu__entry"><Link to={this.props.url}>{this.props.label}</Link></div>
        }
    }
}

export class SideMenu extends React.Component<SideMenuProps> {
    render_entries() {
        let menu = [];
        for (let entry of this.props.entries) {
            menu.push(<SideMenuEntry {...entry}/>);
        }
        return menu;
    }
    render() {
        return <div className="side_menu">
            {this.render_entries()}
        </div>
    }
}