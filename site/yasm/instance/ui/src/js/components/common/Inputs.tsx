import * as React from 'react';
import '../../../scss/inputs/index.scss';
import {MonacoWrapper} from "./MonacoWrapper";
import {jsJsx} from "ts-loader/dist/types/constants";

interface InputsProps {
    onChange?: (event: any) => void
    name?: string
    className?: string
    placeholder?: string
    disabled?: boolean
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
                disabled={this.props.disabled}
                value={this.props.text}
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
                disabled={this.props.disabled}
                value={this.props.password}
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
                    disabled={this.props.disabled}
                />
            </div>
        )
    }
}

interface ChoiceInputProps {
    choice: string
    choices: string[]
}

export class ChoiceInput extends React.Component<ChoiceInputProps & InputsProps> {
    render() {
        return (
            <select
                onChange={this.props.onChange}
                disabled={this.props.disabled}
                value={this.props.choice}
            >
                {this.props.choices.map(choice => (
                    <option>
                        {choice}
                    </option>
                ))}
            </select>
        )
    }
}


interface JSONInputProps {
    json: string
}

export class JSONInput extends React.Component<JSONInputProps & InputsProps> {
    render() {
        return (
            <MonacoWrapper
                value={this.props.json}
                onChange={this.props.onChange}
                width={300}
                height={500}
                options={this.props.disabled? {
                    readOnly: true
                }: {}}
            />
        )
    }
}

export type InputTypes = 'text' | 'string' | 'JSON' | 'number' | 'choice'
interface InputProps {
    type: InputTypes
    props: (TextInputProps | PasswordInputProps | StringInputProps | JSONInputProps | ChoiceInputProps) & InputsProps
}

export class Input extends React.Component<InputProps> {
    render(): React.ReactElement<any, string | React.JSXElementConstructor<any>> | string | number | {} | React.ReactNodeArray | React.ReactPortal | boolean | null | undefined {
        switch (this.props.type) {
            case 'choice':
                return <ChoiceInput {...this.props.props as any}/>
            case 'string':
                return <StringInput {...this.props.props as any}/>
            case 'text':
                return <TextInput {...this.props.props as any}/>
            case 'number':
                return <StringInput {...this.props.props as any}/>
            case 'JSON':
                return <JSONInput {...this.props.props as any}/>
        }
    }
}
