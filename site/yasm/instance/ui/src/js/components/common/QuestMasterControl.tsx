import * as React from 'react'
import {connect} from 'react-redux'
import {faTasks} from '@fortawesome/free-solid-svg-icons/faTasks'
import {FontAwesomeIcon as FAIcon} from '@fortawesome/react-fontawesome'
import { commonActions, CommonState, TopRightPanels } from '../../redux-structure/common'
import { ReduxProps } from '../../redux-structure/store'
import { Dot } from './Dot'
import { QuestMaster } from './QuestMaster'


import '../../../scss/quest-maser-control/index.scss'


@(connect((state: any) => state.common) as any)
export class QuestMasterControl extends React.Component<CommonState & ReduxProps> {
    render(): React.ReactNode {
        if (this.props.login.loggedIn !== true) {
            return null
        } else {
            return (
                <div className="quest-master-control" onClick={ () => this.props.dispatch(commonActions.common.panel.topRight.toggle(TopRightPanels.QUESTS)) }>
                    <FAIcon icon={ faTasks } className="quest-master-control__icon" />
                    <Dot/>
                    <QuestMaster/>
                </div>
            )
        }
    }
}
