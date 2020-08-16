import * as React from 'react'
import {Provider, Store} from 'react-redux'
import {TopMenu} from '../components/common/TopMenu'
import {Router} from 'react-router-dom'
import {BugReporter} from '../components/common/BugReporter'
import {getStore} from '../redux-structure/store'
import {commonActions, CommonState} from '../redux-structure/common'

import {history} from '../util/history'
import {Spinner} from "../components/common";

interface BasePageProps {
    reducerMap?: any
    initialState?: any
    initialCommonState?: CommonState
}

interface Changable {
    idx: boolean,
}

export class BasePage extends React.Component<BasePageProps, Changable> {
    static defaultProps = {
        reducerMap: {},
        initialState: {},
        initialCommonState: {},
    }

    store = null as Store<any>

    constructor(props: BasePageProps) {
        super(props)
        this.store = getStore(this.props.reducerMap, this.props.initialState, this.props.initialCommonState)
        this.store.dispatch(commonActions.common.login.fetch())
        this.state = {
            idx: false,
        }
    }

    componentDidMount(): void {
        this.store.subscribe(() => this.setState({
            idx: ! this.state.idx
        }))
    }

    render() {
        return (
            <Provider store={ this.store }>
                <Router history={ history }>
                    <React.Fragment>
                        <TopMenu/>
                        {
                            this.store.getState().common.login.profile !== undefined
                            ? this.props.children
                            : <Spinner/>
                        }
                        <BugReporter/>
                    </React.Fragment>
                </Router>
            </Provider>
        )
    }
}
