import * as React from 'react'
import * as Color from 'color'

import '../../../scss/button/index.scss'

interface ButtonProps {
    style: 'green' | 'action' | 'gray' | 'cancel'
    type?: 'submit' | 'reset' | 'button'
    className?: string
    onClick: (event: React.MouseEvent) => void
}

export class Button extends React.Component<ButtonProps> {
    getStyle() {
        let c
        switch (this.props.style) {
            case "action":
            case "green":
                c = Color('#9bff69')
                break
            case "cancel":
            case "gray":
                c = Color('#b3b3b3')
                break
        }

        return {
            '--button-default-color': c.rgb().string(),
            '--button-hover-color': c.lighten(0.1).rgb().string(),
            '--button-active-color': c.lighten(0.2).rgb().string(),
            '--button-active-border-color': c.rgb().string(),
        } as React.CSSProperties
    }

    render() {
        return (
            <button
                onClick={this.props.onClick}
                style={this.getStyle()}
                type={this.props.type}
                className={'button ' + this.props.className }
            >
                {this.props.children}
            </button>
        )
    }
}
