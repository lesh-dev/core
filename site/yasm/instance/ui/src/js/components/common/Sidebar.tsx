import * as React from "react";
import {connect} from "react-redux";
import {ReduxProps} from "../../redux-structure/store";
import {sidebarActions, SidebarEntry, SidebarEntryType, SidebarState} from "../../redux-structure/sidebar";
import {Link} from "react-router-dom";
import {Dropdown} from "./Dropdown";
import { faTimesCircle } from "@fortawesome/free-regular-svg-icons/faTimesCircle";
import { FontAwesomeIcon as FAIcon } from '@fortawesome/react-fontawesome'
import { faArrowRight } from '@fortawesome/free-solid-svg-icons/faArrowRight'
import { faArrowLeft } from '@fortawesome/free-solid-svg-icons/faArrowLeft'


import '../../../scss/sidebar/sidebar.scss'

@(connect((state: any) => state.common.sidebar) as any)
export class Sidebar extends React.Component<SidebarState & ReduxProps> {
    private render_icon(entry: SidebarEntry) {
        return entry.image === null
            ? null
            : <FAIcon icon={
                entry.image === undefined
                    ? faTimesCircle
                    : entry.image
            }/>
    }
    private render_entry(entry: SidebarEntry) {
        const cls = 'sidebar__display' + (this.props.collapsed ? ' sidebar__display--collapsed' : '')
        switch (entry.type) {
            case SidebarEntryType.Link:
                return <Link to={entry.url} className="sidebar__entry" >
                    {
                        this.render_icon(entry)
                    }
                    <div className={ cls }>
                        {
                            entry.display
                        }
                    </div>
                </Link>
            case SidebarEntryType.Folder:
                return <>  /// TODO (rebenkoy)
                    {
                        this.render_icon(entry)
                    }
                    <Dropdown label={() => entry.display} component={() => <div/>}/>
                </>
            case SidebarEntryType.ActionButton:
                return <div
                    onClick={() => this.props.dispatch(entry.action)}
                    className="sidebar__entry"
                >
                    {
                        this.render_icon(entry)
                    }
                    <div className={ cls }>
                        {
                            entry.display
                        }
                    </div>
                </div>
            case SidebarEntryType.SuperButton:
                if (this.props.collapsed) {
                    entry.display = 'Открыть'
                    entry.image = faArrowRight
                } else {
                    entry.display = 'Закрыть'
                    entry.image = faArrowLeft
                }
                return <div
                    onClick={() => this.props.dispatch(sidebarActions.common.sidebar.toggle())}
                    className="sidebar__entry"
                >
                    {
                        this.render_icon(entry)
                    }
                    <div className={ cls }>
                        {
                            entry.display
                        }
                    </div>
                </div>

            case SidebarEntryType.Spacer:
                return <div style={{flexGrow: 10}}/>
        }
    }

    render(): React.ReactNode {
        if (this.props.entries.length == 0) {
            return null
        }
        return <>
            <div
                id="sidebar"
                className={ this.props.collapsed ? 'sidebar--collapsed' : '' }
            >

                {
                    this.render_entry({
                        type: SidebarEntryType.SuperButton,
                    })
                }
                {
                    this.props.entries.map(entry =>
                        this.render_entry(entry)
                    )
                }
            </div>
        </>
    }
}
