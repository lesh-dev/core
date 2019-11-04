import * as React from 'react'
import {connect} from 'react-redux'
import {Link} from 'react-router-dom'
import {CommonState} from '../../redux-structure/common'
import {ReduxProps} from '../../redux-structure/store'

// @ts-ignore
import Incognito from '../../../assets/incognito.svg' // I know what I am doing (c) Yar-R


@(connect((state: any) => state.common) as any)
export class PersonalButton extends React.Component<CommonState & ReduxProps> {
    render() {
        if (this.props.login.loggedIn === true) {
            if (document.location.pathname.startsWith('/i')) {
                return (
                    <Link
                        to="/i"
                    >
                        <Incognito height="35" width="35" fill="red"/>
                    </Link>
                )
            } else {
                return (
                    <a href={'/i/'}>
                        <Incognito height="35" width="35" fill="red"/>
                    </a>
                )
            }
        } else {
            return (
                <a href={'/login/'}>
                    <Incognito height="35" width="35"/>
                </a>
            )
        }
    }
}
