import * as React from 'react';
import {LoginForm} from "../forms/login";
import {LoginOauth} from "./LoginOauth";

import '../../../scss/login-pocket/index.scss'

interface LoginPocketProps {
    unscaled_width?: number
    scale?: number
    background?: string
    triangle_size?: number
    spacer_height?: number
    padding?: number
    button_default_color?: string
    button_hover_color?: string
    button_active_color?: string
    button_active_border_color?: string
}

export class LoginPocket extends React.Component<LoginPocketProps, undefined> {
    static defaultProps = {
        background: 'rgba(173, 255, 47, 0.56)',
        triangle_size: 20,
        spacer_height: 5,
        padding: 5,
        unscaled_width: 300,
        scale: 1,
    };

    render(): JSX.Element {
        return (
            <div style={
                {
                    'width': this.props.unscaled_width * this.props.scale,
                    '--background': this.props.background,
                    '--triangle-size': `${this.props.triangle_size}px`,
                    '--spacer_height': `${this.props.spacer_height}px`,
                    '--padding': `${this.props.padding}px`,
                } as React.CSSProperties
            }>
                <div className={'login-pocket'}>
                    <LoginForm scale={this.props.scale}/>
                    <div className={'login-pocket__spacer'}/>
                    <LoginOauth/>
                    <div className={'login-pocket__spacer'}/>
                    <div className={'login-pocket__spacer'}/>
                </div>
                <div className={'login-pocket__footer'}/>
            </div>
        )
    }
}
