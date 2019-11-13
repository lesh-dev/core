import * as React from 'react'

import '../../../../scss/top-right-panel/index.scss'

export class TopRightPanel extends React.Component{
    render() {
        return <div className="top-right-panel">{ this.props.children } </div>
    }
}