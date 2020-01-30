import * as React from 'react'
import {FontAwesomeIcon as FAIcon} from "@fortawesome/react-fontawesome";
import {faEdit} from "@fortawesome/free-regular-svg-icons/faEdit";
import {faTimesCircle} from "@fortawesome/free-regular-svg-icons/faTimesCircle";
import {faCheck} from "@fortawesome/free-solid-svg-icons/faCheck";

import "../../../scss/edit/edit.scss"

export interface EditProps {
    edit: boolean
    onClick: () => void,
    exit?: boolean,
    onExit?: () => void,
    submit?: boolean,
    onSubmit?: () => void,

    className?: string,
    id?: string,
    style?: React.CSSProperties,
    pad?: boolean,
}


export class Edit extends React.Component<EditProps, undefined> {
    static defaultProps = {
        submit: false,
        onSubmit: () => {},
        exit: false,
        onExit: () => {},
    }

    private render_edit() {
        return <div
            onClick={this.props.onClick}
            className="edit__button"
        >
            <FAIcon icon={faEdit}/>
        </div>
    }

    private render_exit() {
        return <div
            onClick={this.props.onExit}
            className="edit__button"
        >
            <FAIcon icon={faTimesCircle}/>
        </div>
    }

    private render_submit() {
        return <div
            onClick={this.props.onSubmit}
            className="edit__button"
        >
            <FAIcon icon={faCheck}/>
        </div>
    }

    render() {
        return <div
            className={'edit ' + (this.props.pad !== undefined && this.props.edit ? 'edit--padded ' : '') + (this.props.className !== undefined ? this.props.className : '')}
            style={this.props.style}
        >
            {
                this.props.children
            }
            <div
                style={{
                    position: 'absolute',
                    top: 0,
                    right: 0,
                }}
            >
                {
                    this.props.edit
                        ? this.render_edit()
                        : null
                }
                {
                    this.props.exit
                        ? this.render_exit()
                        : null
                }
                {
                    this.props.submit
                        ? this.render_submit()
                        : null
                }
            </div>
        </div>
    }
}