import * as React from 'react';
import '../../../scss/inputs/index.scss';

interface InputsProps {
    onChange: (event: any) => void
    name?: string
    className?: string
    placeholder?: string
}

interface StringInputProps {
    text: string
}

export class StringInput extends React.Component<StringInputProps & InputsProps> {
    render() {
        return (
            <input
                className={'inputs ' + this.props.className}
                onChange={event => this.props.onChange(event)}
                name={this.props.name}
                placeholder={this.props.placeholder}
            />
        )
    }
}

interface PasswordInputProps {
    password: string
}

export class PasswordInput extends React.Component<PasswordInputProps & InputsProps> {
    render() {
        return (
            <input
                className={'inputs ' + this.props.className}
                type={'password'}
                onChange={event => this.props.onChange(event)}
                name={this.props.name}
                placeholder={this.props.placeholder}
            />
        )
    }
}

interface TextInputProps {
    text: string
}

export class TextInput extends React.Component<TextInputProps & InputsProps> {
    render() {
        return (
            <div style={{paddingRight: '5px'}}>
                <textarea
                    onChange={event => this.props.onChange(event)}
                    name={this.props.name}
                    className={'inputs ' + this.props.className}
                    value={this.props.text}
                    placeholder={this.props.placeholder}
                />
            </div>
        )
    }
}
