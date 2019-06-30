import * as React from 'react'
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faBug, faTimes} from "@fortawesome/free-solid-svg-icons";
import {BugReporterForm} from "../forms/BugReporter";
import {Button} from "./Button";

import '../../../scss/bug-reporter/bug-reporter.scss'

interface BugReporterState {
    opened: boolean
}

export class BugReporter extends React.Component<{}, BugReporterState>{
    constructor(props: any) {
        super(props)
        this.state = {
            opened: false
        }
    }

    renderToggler() {
        return (
            <div className={'bug-reporter__toggler'} onClick={() => this.setState({opened: !this.state.opened})}>
                <div style={{position: 'absolute', zIndex: -1}}>
                    <svg style={{width: '50px', height: '40px'}}>
                        <polygon points="0,0 40,0 50,20 40,40 0,40" style={{fill: 'lightgray'}}/>
                    </svg>
                </div>
                <div style={{padding: '4px', paddingRight: '14px'}}>
                    <FontAwesomeIcon icon={faBug} color={'coral'} size={'2x'}/>
                </div>
            </div>
        )
    }

    renderContent() {
        if (!this.state.opened) {
            return this.renderToggler()
        }
        return (
            <div className={'bug-reporter__modal'}>
                <div className={'bug-reporter__header'}>
                    {this.renderToggler()}
                    <span className={'bug-reporter__heading'}>
                        Сообщить об ошибке
                    </span>
                    <Button
                        onClick={() => this.setState({opened: false})}
                        style={'action'}
                        type='submit'
                    >
                        <FontAwesomeIcon icon={faTimes}/>
                    </Button>
                </div>
                <BugReporterForm onCancel={() => this.setState({opened: false})}/>
            </div>
        )
    }

    render() {
        return (
            <div className={'bug-reporter'} style={{width: this.state.opened? '100%': '50px'}}>
                {this.renderContent()}
            </div>
        )
    }
}
