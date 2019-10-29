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
                <div>
                    <StringInput
                        text={this.state.login}
                        name={'login'}
                        placeholder={'логин'}
                        onChange={event => this.handle_login_change(event)}
                    />
                </div>
                <div>
                    <PasswordInput
                        password={this.state.password}
                        name={'password'}
                        placeholder={'пароль'}
                        onChange={event => this.handle_password_change(event)}
                    />
                </div>
            </React.Fragment>
        )
    }

    handle_response(): void {
        redirect('/i/')
    }
}
