import * as React from 'react'
import { connect } from 'react-redux'
import { commonActions, CommonState, TopRightPanels } from '../../redux-structure/common'
import { ReduxProps } from '../../redux-structure/store'
import { faSignOutAlt } from '@fortawesome/free-solid-svg-icons/faSignOutAlt'

import { VerticalMenu } from './VerticalMenu'
import { history } from '../../util/history'

// @ts-ignore // I know what I am doing (c) Yar-R
import Incognito from '../../../assets/incognito.svg'


@(connect((state: any) => state.common) as any)
export class PersonalButton extends React.Component<CommonState & ReduxProps> {
    renderPanel() {
        return (
            <VerticalMenu
                style={{
                    position: 'fixed',
                    right: '32px',
                }}
                entries={
                    [
                        {
                            title: 'Моя страница',
                            callback: () => history.push('/i/'),
                        },
                        {
                            title: 'выйти',
                            icon: faSignOutAlt,
                            callback: () => this.props.dispatch(commonActions.common.login.exit()),
                        },
                    ]
                }
            />
        )
    }

    render() {
        if (this.props.login.loggedIn === true) {
            return (
                <div>
                    <div onClick={ () => this.props.dispatch(commonActions.common.panel.topRight.toggle(TopRightPanels.PERSONAL)) }>
                        <Incognito height="35" width="35" fill="red"/>
                    </div>
                    {
                        this.props.panel.topRight.current === TopRightPanels.PERSONAL
                            ? this.renderPanel()
                            : null
                    }
                </div>
            )
        } else {
            return (
                <a href={'/login/'}>
                    <Incognito height="35" width="35"/>
                </a>
            )
        }
    }
}
