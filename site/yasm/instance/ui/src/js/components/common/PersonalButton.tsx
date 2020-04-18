import * as React from 'react'
import { connect } from 'react-redux'
import { commonActions, CommonState, TopRightPanels } from '../../redux-structure/common'
import { ReduxProps } from '../../redux-structure/store'
import { faSignOutAlt } from '@fortawesome/free-solid-svg-icons/faSignOutAlt'

import { VerticalMenu } from './VerticalMenu'
import { history } from '../../util/history'

// @ts-ignore // I know what I am doing (c) Yar-R
import Incognito from '../../../assets/incognito.svg'
import {TopRightPanel} from "./panels/TopRight";


@(connect((state: any) => state.common) as any)
export class PersonalButton extends React.Component<CommonState & ReduxProps> {
    renderPanel() {
        return (
            <TopRightPanel>
                <VerticalMenu
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
            </TopRightPanel>
        )
    }

    render() {
        if (this.props.login.loggedIn === true) {
            return (
                <div>
                    <div onClick={ () => this.props.dispatch(commonActions.common.panel.topRight.toggle(TopRightPanels.PERSONAL)) }>
                        {
                            this.props.login.profile.ava !== undefined
                            ? <img src={this.props.login.profile.ava} width="35" height="35"/>
                            : <Incognito height="35" width="35" fill="red"/>
                        }
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
