import * as React from 'react'
import '../../../scss/spinner/spinner.scss'

export class Spinner extends React.Component {
    render() {
        return (
            <React.Fragment>
                <div className="spinner"></div>
                <div className="spinner"></div>
                <div className="spinner"></div>
                <div className="spinnerCircle"></div>
            </React.Fragment>
        )
    }
}
