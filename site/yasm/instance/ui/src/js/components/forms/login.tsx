import * as React from 'react';
import {CSRFForm} from "./CSRFform";
import {PasswordInput, StringInput} from "../common/Inputs";

interface LoginFormState {
    login: string,
    password: string
}

export class LoginForm extends CSRFForm<undefined, LoginFormState> {
    constructor(props: any) {
        super(props)
        this.state = {
            login: '',
            password: ''
        }
    }

    handle_login_change(event: React.ChangeEvent<HTMLInputElement>): void {
    }

    handle_password_change(event: React.ChangeEvent<HTMLInputElement>): void {
    }

    render_form(): JSX.Element {
        return (
            <React.Fragment>
                <StringInput
                    text={ this.state.login }
                    name={ 'login' }
                    onChange={ event => this.handle_login_change(event) }
                />
                <PasswordInput
                    password={ this.state.password }
                    name={ 'login' }
                    onChange={ event => this.handle_password_change(event) }
                />
            </React.Fragment>
        )
    }
}