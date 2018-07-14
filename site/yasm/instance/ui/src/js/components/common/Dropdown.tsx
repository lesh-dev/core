import * as React from 'react';
import "../../../scss/dropdown/dropdown.scss"

export interface DropdownState {
    openeed: boolean
}

export interface DropdownProps {
    label: string
    component: any
    onExpand?: () => void
}


export class Dropdown extends React.Component<DropdownProps, DropdownState> {
    constructor(props: any) {
        super(props);
        this.state = {
            openeed: false,
        }
    }

    toggle() {
        this.setState({openeed: !this.state.openeed})
    }

    render_label() {
        return <div onClick={() => {
            this.toggle()
        }}>
            {this.props.label}
        </div>
    }

    render() {
        return <div className="dropdown">
            {this.render_label()}
            <div className="dropdown__content">
                {this.state.openeed ? this.props.component : null}
            </div>
        </div>
    }
}
