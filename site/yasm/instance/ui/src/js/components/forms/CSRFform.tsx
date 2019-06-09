import * as React from 'react';
import * as Cookies from 'es-cookie';


export class CSRFForm<P, S> extends React.Component<P, S> {
    render() {
        return (
            <React.Fragment>
                <input type="hidden" name="_csrf" value={ Cookies.get('XSRF-COOKIE') || 'TODO' }/>
                { this.render_form() }
                { this.render_submit() }
            </React.Fragment>
        )
    }

    render_form(): JSX.Element {
        return null
    }

    render_submit() {
        return (
            <div
                onClick={ () => this.submit() }
                className={ 'form__submit' }
            >
                Отправить
            </div>
        )
    }

    submit(): null {
        return null
    }
}