import * as React from 'react';

export interface CutState {
    opened: boolean
}

export interface CutProps {
    label: string
    content: any
}

export class Cut extends React.Component<CutProps, CutState> {
    constructor(props: any) {
        super(props);
        this.state = {
            opened: false
        }
    }

    render_under() {
        if (this.state.opened) {
            return this.props.content.render()
        } else {
            return null
        }
    }

    on_click() {
        this.setState({opened: !this.state.opened})
    }

    render_button() {
        if (this.state.opened) {
            return <div className={"cut__button"} onClick={() => {
                this.on_click()
            }}>▲</div>
        } else {
            return <div className={"cut__button"} onClick={() => {
                this.on_click()
            }}>▼</div>
        }
    }

    render() {
        return <div className={"cut"}>
            <div className={"cut__bar"}>
                <div className={"cut__label"}>
                    {this.props.label}
                </div>
                <div className={"cut__hbar"}>
                    <div></div>
                    <div></div>
                </div>
                {this.render_button()}
            </div>
            {this.render_under()}
        </div>
    }
}