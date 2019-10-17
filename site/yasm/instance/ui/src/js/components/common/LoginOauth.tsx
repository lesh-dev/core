import * as React from 'react';
import '../../../scss/login-oauth/index.scss'

export class LoginOauth extends React.Component {
    render() {
        return (
            <div className={'login-oauth'}>
                <img
                    className={'login-oauth__button'}
                    src={'/static/emblems/oauth/Facebook.svg'}
                />
                <img
                    className={'login-oauth__button'}
                    src={'/static/emblems/oauth/Google.svg'}
                />
                <img
                    className={'login-oauth__button'}
                    src={'/static/emblems/oauth/VK.svg'}
                />
                <img
                    className={'login-oauth__button'}
                    src={'/static/emblems/oauth/Yandex.svg'}
                />
            </div>
        )
    }
}
