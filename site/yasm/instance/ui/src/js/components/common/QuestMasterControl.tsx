import * as React from 'react'
import { connect } from 'react-redux'
import { faTasks } from '@fortawesome/free-solid-svg-icons/faTasks'
import { FontAwesomeIcon as FAIcon } from '@fortawesome/react-fontawesome'
import { commonActions } from '../../redux-structure/common'


import { CommonState } from '../../redux-structure/common'
import { ReduxProps } from '../../redux-structure/store'
import { Dot } from './Dot'

import '../../../scss/quest-maser-control/index.scss'


@(connect((state: any) => state.common) as any)
export class QuestMasterControl extends React.Component<CommonState & ReduxProps> {
    render(): React.ReactNode {
        if (this.props.login.loggedIn !== true) {
            return null
        } else {
            return (
                <div className="quest-master-control" onClick={ () => this.props.dispatch(commonActions.common.questMaster.toggle()) }>
                    <FAIcon icon={ faTasks } className="quest-master-control__icon" />
                    <Dot/>
                </div>
            )
        }
    }
}
