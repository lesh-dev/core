import * as React from 'react'
import {Input, InputTypes} from "./Inputs";

interface FieldProps {
    name: string
    type: InputTypes | 'function' | 'object'
    choices?: string[]
    default?: string | number | (() => void)
}

interface ExampleProps {
    fields: FieldProps[]
    renderer: (props: any) => React.ReactNode
}

interface ExampleState {
    componentState: any
    opened: boolean
}

export class Example extends React.Component<ExampleProps, ExampleState> {
    constructor(props: ExampleProps) {
        super(props)

        this.state = {
            opened: false,
            componentState: {}
        }
        let p = {} as any
        for (const field of props.fields) {
            switch (field.type) {
                case 'function':
                    p[field.name] = field.default || console.log
                    break
                case 'JSON':
                case 'object':
                    p[field.name] = JSON.parse(field.default as string || "{}")
                    break
                case 'number':
                    p[field.name] = field.default || 0
                    break
                default:
                    p[field.name] = field.default || ''
            }
        }
        this.state = {
            opened: this.state.opened,
            componentState: p
        }
    }

    renderField(field: FieldProps) {
        switch(field.type) {
            case "function":
                return <Input
                    type={'string'}
                    props={{
                        text: (this.state.componentState[field.name] || console.log).toString(),
                        disabled: true
                    }}
                />
            case "object":
                return <Input
                    type={'JSON'}
                    props={{
                        json: JSON.stringify(this.state.componentState[field.name], undefined, 2),
                        disabled: true
                    }}
                />
            case "JSON":
                return <Input
                    type={field.type}
                    props={{
                        json: JSON.stringify(this.state.componentState[field.name], undefined, 2),
                        onChange: text => {
                            let p = {} as any
                            p[field.name] = JSON.parse(text)
                            this.setState({
                                componentState: {
                                    ...this.state.componentState,
                                    ...p
                                }
                            })
                        }
                    }}
                />
            case "choice":
                return <Input
                    type={field.type}
                    props={{
                        choice: this.state.componentState[field.name],
                        choices: field.choices,
                        onChange: event => {
                            let p = {} as any
                            p[field.name] = event.target.value
                            this.setState({
                                componentState: {
                                    ...this.state.componentState,
                                    ...p
                                }
                            })
                        }
                    }}
                />
            default:
                return <Input
                    type={field.type}
                    props={{
                        text: this.state.componentState[field.name],
                        onChange: event => {
                            let p = {} as any
                            p[field.name] = event.target.value
                            this.setState({
                                componentState: {
                                    ...this.state.componentState,
                                    ...p
                                }
                            })
                        }
                    }}
                />
        }
    }

    render(): React.ReactElement<any, string | React.JSXElementConstructor<any>> | string | number | {} | React.ReactNodeArray | React.ReactPortal | boolean | null | undefined {
        return (
            <div className={'example'}>
                <div className={'example__component'}>
                    {this.props.renderer(this.state.componentState)}
                </div>
                <div className={'example__control'}>
                    {this.props.fields.map(field => (
                        <div>
                            <div>
                                {field.name}
                            </div>
                            {this.renderField(field)}
                        </div>
                    ))}
                </div>
            </div>
        )
    }
}
