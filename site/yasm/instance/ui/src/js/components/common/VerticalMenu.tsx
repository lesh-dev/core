import * as React from 'react'
import { FontAwesomeIcon as FAIcon } from '@fortawesome/react-fontawesome'
import { IconProp } from '@fortawesome/fontawesome-svg-core'

import '../../../scss/vertical-menu/index.scss'

export interface Entry {
    icon?: IconProp,
    title: string,
    callback?: (title: string) => void,
}

export interface VerticalMenuProps {
    entries: Entry[],
    style?: React.CSSProperties,
}

export class VerticalMenu extends React.Component<VerticalMenuProps> {
    renderEntry(entry: Entry): React.ReactNode {
        const pointer: React.CSSProperties = entry.callback !== undefined
            ? {
                cursor: 'pointer',
            }
            : {}
        return (
            <div
                key={entry.title}
                className="vertical-menu__entry"
                onClick={
                    () => {
                        if (entry.callback !== undefined) {
                            entry.callback(entry.title)
                        }
                    }
                }
                style={ pointer }
            >
                { entry.title }
                {
                    entry.icon !== undefined
                        ? <FAIcon icon={ entry.icon }/>
                        : null
                }
            </div>
        )
    }

    render(): React.ReactNode {
        return (
            <div
                className="vertical-menu"
                style={ this.props.style || {} }
            >
                {
                    this.props.entries.map(e => this.renderEntry(e))
                }
            </div>
        )
    }
}
