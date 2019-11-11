import * as React from 'react'
import {connect, Provider} from 'react-redux'
import {TopMenu} from '../components/common/TopMenu'
import {Router} from 'react-router-dom'
import {BugReporter} from '../components/common/BugReporter'
import {getStore} from '../redux-structure/store'
import {commonActions} from '../redux-structure/common'
import {QuestMaster} from "../components/common/QuestMaster";

import { history } from '../util/history'

interface BasePageProps {
    reducerMap?: any
    initialState?: any
}

export class BasePage extends React.Component<BasePageProps> {
    static defaultProps = {
        reducerMap: {},
        initialState: {},
        page_renderer: () => null as React.ReactNode
    }

    constructor(props: BasePageProps) {
        super(props)
    }

    render() {
        const store = getStore(this.props.reducerMap, this.props.initialState)
        store.dispatch(commonActions.common.login.fetch())
        return (
            <Provider store={ store }>
                <Router history={ history }>
                    <React.Fragment>
                        <TopMenu/>
                        {this.props.children}
                        <QuestMaster/>
                        <BugReporter/>
                    </React.Fragment>
                </Router>
            </Provider>
        )
    }
}
