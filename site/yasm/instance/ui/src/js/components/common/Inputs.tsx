import * as React from 'react';
import '../../../scss/inputs/index.scss';

interface InputsProps {
    onChange: (event: any) => void
    display_name?: string
    name?: string
    className?: string
    onBlur?: (event: React.FocusEvent<HTMLDivElement>) => void
    onFocus?: (event: React.FocusEvent<HTMLDivElement>) => void
}

export class Inputs<P> extends React.Component<InputsProps & P> {
    static defaultProps = {
        onBlur: (event: any) => {},
        onFocus: (event: any) => {},
    };

    render() {
        return (
            <React.Fragment>
                <div
                    onBlur={event => this.props.onBlur(event)}
                    onFocus={event => this.props.onFocus(event)}
                    className={`inputs ${this.props.className || ''}`}
                >
                    <div className={'inputs__display-name'}>
                        {this.props.display_name}
                    </div>
                    <div className={'inputs__horizontal-spacer'}/>
                    <div className={'inputs__input'}>
                        {this.render_value()}
                        {this.render_input()}
                    </div>
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
}

interface TextInputProps {
    text: string
    onChange: (event: React.ChangeEvent<HTMLTextAreaElement>) => void
    name: string
}

export class TextInput extends React.Component<TextInputProps> {
    render() {
        return (
            <div style={{paddingRight: '5px'}}>
                <textarea
                    onChange={event => this.props.onChange(event)}
                    name={this.props.name}
                    className={'inputs'}
                    value={this.props.text}
                />
            </div>
        )
    }
}
