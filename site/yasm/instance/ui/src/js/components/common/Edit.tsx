import * as React from 'react'
import {FontAwesomeIcon as FAIcon} from "@fortawesome/react-fontawesome";
import {faEdit} from "@fortawesome/free-regular-svg-icons/faEdit";
import {faCheck} from "@fortawesome/free-solid-svg-icons/faCheck";

import "../../../scss/edit/edit.scss"

export interface EditProps {
    show: boolean
    onClick: () => void,
    submit?: boolean,
    onSubmit?: () => void,

    className?: string,
    id?: string,
    style?: React.CSSProperties,
}


export class Edit extends React.Component<EditProps, undefined> {
    defaultProps = {
        submit: false,
        onSubmit: () => {}
    }
    private render_edit() {
        return <div
            onClick={this.props.onClick}
            className="edit__button"
        >
            <FAIcon icon={faEdit}/>
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
            className={'edit ' + (this.props.className !== undefined ? this.props.className : '')}
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
                    this.props.show
                        ? this.render_edit()
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