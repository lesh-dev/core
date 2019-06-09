import * as React from 'react';
import {Simulate} from "react-dom/test-utils";
import input = Simulate.input;

interface InputsProps {
    onChange: (event: React.ChangeEvent<HTMLInputElement>) => void
    display?: string
    name?: string
    className?: string
    onBlur?: (event: React.FocusEvent<HTMLDivElement>) => void
    onFocus?: (event: React.FocusEvent<HTMLDivElement>) => void
}

export class Inputs<P> extends React.Component<InputsProps & P> {
    static defaultProps = {
        onBlur: (event: any) => {},
        onFocus: (event: any) => {},
    }

    render() {
        return (
            <React.Fragment>
                <div
                    onBlur={event => this.props.onBlur(event)}
                    onFocus={event => this.props.onFocus(event)}
                    className={'input ' + this.props.className}
                >
                    <div>
                        {this.props.display}
                    </div>
                    {this.render_value()}
                    {this.render_input()}
                </div>
            </React.Fragment>
        )
    }

    render_input(): JSX.Element {
        return null
    }

    render_value(): JSX.Element {
        return null
    }
}

interface StringInputProps {
    text: string
}

export class StringInput extends Inputs<StringInputProps> {
    render_input() {
        return (
            <input
                onChange={event => this.props.onChange(event)}
                name={this.props.name}
            />
        )
    }

    render_value(): JSX.Element {
        return (
            <React.Fragment>
                {this.props.text}
            </React.Fragment>
        )
    }

}

interface PasswordInputProps {
    password: string
}

export class PasswordInput extends Inputs<PasswordInputProps> {
    render_input() {
        return (
            <input
                type={'password'}
                onChange={event => this.props.onChange(event)}
                name={this.props.name}
            />
        )
    }

    render_value(): JSX.Element {
        return (
            <React.Fragment>
                {'*'.repeat(this.props.password.length)}
            </React.Fragment>
        )
    }
}