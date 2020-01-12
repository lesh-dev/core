import * as React from 'react';
import "../../../scss/dropdown/dropdown.scss"
import {faArrowAltCircleDown, faArrowAltCircleUp} from "@fortawesome/free-regular-svg-icons";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";

export interface DropdownState {
    openeed: boolean
}

export interface DropdownProps {
    label: () => React.ReactNode
    component: () => React.ReactNode
    onExpand?: () => void
    onCollapse?: () => void
    type?: 'click' | 'hover'
    className?: string
}


export class Dropdown extends React.Component<DropdownProps, DropdownState> {
    static defaultProps = {
        type: 'click',
        onExpand: () => {
        },
        onCollapse: () => {
        },
        className: '',
    };

    constructor(props: any) {
        super(props);
        this.state = {
            openeed: false,
        }
    }

    toggle() {
        if (this.state.openeed) {
            this.props.onCollapse();
        } else {
            this.props.onExpand();
        }
        this.setState({openeed: !this.state.openeed})
    }

    render_label() {
        return <div
            onClick={() => {
                if (this.props.type === 'click') {
                    this.toggle();
                }
            }}
            style={{display: 'flex'}}
        >
            {this.props.label()}
            <FontAwesomeIcon icon={this.state.openeed ? faArrowAltCircleUp :faArrowAltCircleDown}/>
        </div>
    }

    render() {
        return (
            <div
                className={this.props.className}
                onMouseEnter={() => {
                    if (this.props.type === 'hover' && !this.state.openeed) {
                        this.toggle();
                    }
                }}
                onMouseLeave={() => {
                    if (this.props.type === 'hover' && this.state.openeed) {
                        this.toggle();
                    }
                }}
            >
                {this.render_label()}
                <div>
                    {this.state.openeed ? this.props.component() : null}
                </div>
            </div>
        )
    }
}
