import * as React from 'react';

import {CSRFForm, CSRFFormProps} from "./CSRFform";
import {PasswordInput, StringInput} from "../common/Inputs";
import {redirect} from "../common/utils";

interface LoginFormState {
    login: string,
    password: string,
}

export class LoginForm extends CSRFForm<{}, LoginFormState> {
    static defaultProps = {
        ...{
            formTarget: '/login/',
        }, ...CSRFForm.defaultProps
    };

    constructor(props: CSRFFormProps) {
        super(props);
        this.state = {
            login: '',
            password: ''
        }
    }

    handle_login_change(event: React.ChangeEvent<HTMLInputElement>): void {
        this.setState({login: event.target.value})
    }

    handle_password_change(event: React.ChangeEvent<HTMLInputElement>): void {
        this.setState({password: event.target.value})
    }

    render_form(): JSX.Element {
        return (
            <React.Fragment>
                <StringInput
                    text={this.state.login}
                    name={'login'}
                    display_name={'логин'}
                    onChange={event => this.handle_login_change(event)}
                />
                <PasswordInput
                    password={this.state.password}
                    name={'password'}
                    display_name={'пароль'}
                    onChange={event => this.handle_password_change(event)}
                />
            </React.Fragment>
        )
    }

    handle_response(): void {
        redirect('/internal/')
    }
}
