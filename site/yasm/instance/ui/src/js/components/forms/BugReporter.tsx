import * as React from 'react';

import {CSRFForm, CSRFFormProps} from "./CSRFform";
import {TextInput} from "../common/Inputs";
import {Button} from "../common/Button";

interface BugReporterFormState {
    what: string,
    how: string,
}

interface BugReporterProps {
    onCancel: () => void
}

export class BugReporterForm extends CSRFForm<BugReporterProps, BugReporterFormState> {
    static defaultProps = {
        ...{
            formTarget: '/bug-reporter/',
        }, ...CSRFForm.defaultProps
    };

    constructor(props: CSRFFormProps & BugReporterProps) {
        super(props);
        this.state = {
            what: `Что случилось?\n`,
            how: `Как это случилось?\n`
        }
    }

    handle_what_change(event: React.ChangeEvent<HTMLTextAreaElement>): void {
        this.setState({what: event.target.value})
    }

    handle_how_change(event: React.ChangeEvent<HTMLTextAreaElement>): void {
        this.setState({how: event.target.value})
    }

    render_form(): JSX.Element {
        return (
            <React.Fragment>
                <TextInput
                    text={this.state.what}
                    name={'whatTheBuzz'}
                    onChange={event => this.handle_what_change(event)}
                />
                <TextInput
                    text={this.state.how}
                    name={'tellMeWhatsHappening'}
                    onChange={event => this.handle_how_change(event)}
                />
            </React.Fragment>
        )
    }

    render_submit() {
        return (
            <React.Fragment>
                <Button
                    style={'action'}
                    type='submit'
                    onClick={event => this.submit(event)}
                    className={'form__submit'}
                >
                    Отправить
                </Button>
                <Button
                    style={'gray'}
                    type='button'
                    onClick={this.props.onCancel}
                    className={'form__submit'}
                >
                    Отменить
                </Button>
            </React.Fragment>
        )
    }

    handle_response(): void {
        alert('Ня кря')
    }
}
