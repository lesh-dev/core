import * as  React from 'react'
import { connect } from 'react-redux'
import { Table, Column } from 'react-virtualized'
import 'react-virtualized/styles.css';

import { FontAwesomeIcon as FAIcon } from '@fortawesome/react-fontawesome'
import { faQuestionCircle } from '@fortawesome/free-regular-svg-icons/faQuestionCircle'
import { faCheckCircle } from '@fortawesome/free-regular-svg-icons/faCheckCircle'
import { faTimesCircle } from '@fortawesome/free-regular-svg-icons/faTimesCircle'
import { faClock } from '@fortawesome/free-regular-svg-icons/faClock'
import { faRegistered } from '@fortawesome/free-regular-svg-icons/faRegistered'
import { faExclamationCircle } from '@fortawesome/free-solid-svg-icons/faExclamationCircle'

import { Modal } from './Modal'
import { CommonState, TopRightPanels } from '../../redux-structure/common'
import { ReduxProps } from '../../redux-structure/store'
import { TopMenu } from './TopMenu'

import '../../../scss/modal/index.scss'
import {TopRightPanel} from "./panels/TopRight";


enum QuestStatus {
    OK,
    BAD,
    REGISTERED,
    IN_PROGRESS,
    NOT_SARTED,
}

class StatusSelect {
    render() {

    }
}

interface QuestMasterState {
    currentModal?: React.ReactNode,
}

@(connect((state: any) => state.common) as any)
export class QuestMaster extends React.Component<CommonState & ReduxProps, QuestMasterState> {
    private static width = 350
    private static iconWidth = 20
    private static rowHeight = 20

    private static renderStatus(status: QuestStatus): React.ReactNode {
        switch (status) {
            case QuestStatus.OK:
                return <FAIcon icon={ faCheckCircle } style={{ color: 'green' }}/>
            case QuestStatus.BAD:
                return <FAIcon icon={ faTimesCircle } style={{ color: 'brick' }}/>
            case QuestStatus.NOT_SARTED:
                return <FAIcon icon={ faExclamationCircle } style={{ color: 'orange' }}/>
            case QuestStatus.IN_PROGRESS:
                return <FAIcon icon={ faClock } style={{ color: 'yellow' }}/>
            case QuestStatus.REGISTERED:
                return <FAIcon icon={ faRegistered } style={{ color: 'darkcyan' }}/>
        }
    }

    render() {
        const rows = [
            {
                name: 'медкнижка',
                why: 'так надо',
                status: QuestStatus.NOT_SARTED,
            },
            {
                name: 'справка',
                why: 'очень надо',
                status: QuestStatus.BAD,
            }
        ]
        if (this.props.panel.topRight.current !== TopRightPanels.QUESTS) {
            return null
        }
        return (
            <TopRightPanel>
                {
                    this.state !== null && this.state.currentModal !== undefined
                        ? (
                            <Modal onClose={
                                () => this.setState({currentModal: undefined})
                            }>
                                { this.state.currentModal }
                            </Modal>
                        )
                        : null
                }
                <div style={{
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    width: QuestMaster.width,
                }}>
                    <div>
                        What Is Your Quest??
                    </div>
                    <Table
                        height={ QuestMaster.rowHeight * rows.length }
                        width={ QuestMaster.width }
                        rowHeight={ QuestMaster.rowHeight }
                        headerHeight={ QuestMaster.rowHeight }
                        disableHeader
                        rowCount={ rows.length }
                        rowGetter={ ({ index }) => rows[index] }
                        gridStyle={{
                            outline: 'none',
                        }}
                    >
                        <Column
                            width={ QuestMaster.width - 2 * QuestMaster.iconWidth }
                            dataKey="name"
                        />
                        <Column
                            width={ QuestMaster.iconWidth }
                            dataKey="why"
                            cellRenderer={ ({ cellData }) =>
                                <>
                                    <span
                                        onClick={ () => this.setState({ currentModal: cellData }) }
                                    >
                                        <FAIcon
                                            icon={ faQuestionCircle }
                                        />
                                    </span>
                                </>
                            }
                        />
                        <Column
                            width={ QuestMaster.iconWidth }
                            dataKey="status"
                            cellRenderer={ ({ cellData }) => QuestMaster.renderStatus(cellData) }
                        />
                    </Table>
                </div>
            </TopRightPanel>
        )
    }
}
