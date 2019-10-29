import * as React from 'react'

import '../../../scss/spinner/spinner.scss'
import {Dropdown} from "./Dropdown";

import '../../../scss/top-menu/index.scss'
import {PersonalButton} from "./personalButton";
import {QuestMasterControl} from "./QuestMasterControl";


interface IMenuSubEntry {
    title: string,
    url: string,
}

interface IMenuEntry {
    title: string,
    subentries?: IMenuSubEntry[],
    url?: string,
}

interface IMenu {
    menu?: IMenuEntry[],
}

const default_menu: IMenu = {
    menu: [
        {
            title: "Home",
            url: "/public",
        },
        {
            title: "Personal",
            url: "/internal/personal/",
        },
        {
            title: "RC",
            url: "/RC/",
        },
        {
            title: "List",
            subentries: [
                {
                    title: "Home",
                    url: "/public",
                },
                {
                    title: "Api",
                    url: "/api",
                },
                {
                    title: "Admin",
                    url: "/admin",
                }
            ]
        },
        {
            title: "List2",
            subentries: [
                {
                    title: "Home",
                    url: "/public",
                },
                {
                    title: "Api",
                    url: "/api",
                },
                {
                    title: "Admin",
                    url: "/admin",
                }
            ]
        },
    ]
};

export class TopMenu extends React.Component<IMenu> {
    static defaultProps = default_menu;
    static height = 40

    render_subentry(subentry: IMenuSubEntry) {
        return <a href={subentry.url}>{subentry.title}</a>
    }

    render_entry(entry: IMenuEntry) {
        if (entry.url) {
            return (
                <a href={entry.url} className="top-menu__entry">
                    <div>
                        {entry.title}
                    </div>
                </a>
            )
        } else {
            return (
                <Dropdown
                    className="top-menu__entry"
                    label={() => <div>{entry.title}</div>}
                    component={() =>
                        <React.Fragment>
                            {entry.subentries.map(subentry => this.render_subentry(subentry))}
                        </React.Fragment>
                    }/>
            )
        }
    }

    render() {
        return (
            <div className="top-menu">
                <div style={{flexGrow: 1}}/>
                <QuestMasterControl/>
                <PersonalButton/>
            </div>
        )
    }
}
