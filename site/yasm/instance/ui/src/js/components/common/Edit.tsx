import * as React from 'react'
import {FontAwesomeIcon as FAIcon} from "@fortawesome/react-fontawesome";
import {faEdit} from "@fortawesome/free-regular-svg-icons/faEdit";

import "../../../scss/edit/edit.scss"

export interface EditProps {
    show: boolean
    className?: string,
    id?: string,
    style?: React.CSSProperties,
    onClick: () => void,
}


export class Edit extends React.Component<EditProps, undefined> {
    private render_edit() {
        return <div
            onClick={this.props.onClick}
            className="edit__button"
        >
            <FAIcon icon={faEdit}/>
        </div>
    }
    render() {
        return <div className="edit">
            {
                this.props.children
            }
            {
                this.props.show
                    ? this.render_edit()
                    : null
            }
        </div>
    }
}