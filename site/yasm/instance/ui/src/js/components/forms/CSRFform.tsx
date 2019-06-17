import * as React from 'react';
import axios from 'axios';
import {stringify} from 'querystring';

import '../../../scss/form/index.scss'


declare var csrf_token: string;

export interface CSRFFormProps {
    formTarget?: string
    className?: string
    button_default_color?: string
    button_hover_color?: string
    button_active_color?: string
    button_active_border_color?: string
}

export class CSRFForm<P={}, S={}> extends React.Component<CSRFFormProps & P, S> {
    constructor(props: CSRFFormProps & P) {
        super(props);
    }

    static defaultProps = {
        className: '',
        button_default_color: '#63b363',
        button_hover_color: 'lightgreen',
        button_active_color: '#9cff9c',
        button_active_border_color: '#63b363',
    };

    render() {
        return (
            <form
                className={`form ${this.props.className}`}
            >
                {this.render_form()}
                {this.render_submit()}
            </form>
        )
    }

    render_form(): JSX.Element {
        return null
    }

    render_submit() {
        return (
            <button
                style={
                    {
                        '--button-default-color': this.props.button_default_color,
                        '--button-hover-color': this.props.button_hover_color,
                        '--button-active-color': this.props.button_active_color,
                        '--button-active-border-color': this.props.button_active_border_color,
                    } as React.CSSProperties
                }
                type='submit'
                onClick={event => this.submit(event)}
                className={'form__submit'}
            >
                Отправить
            </button>
        )
    }

    submit(event: any): void {
        event.preventDefault();
        axios.request({
            maxRedirects: 0,
            method: 'post',
            data: stringify(this.get_data()),
            url: this.props.formTarget,
            headers: {
                'X-CSRFToken': csrf_token,
                'content-type': 'application/x-www-form-urlencoded',
            },
        }).then(response => this.handle_response())
    }

    get_data(): any {
        return this.state;
    }

    handle_response(): void {

    }
}
