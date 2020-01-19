import * as React from 'react'
import {MonacoWrapper} from "./MonacoWrapper";

export interface ErrorShowProps {
    error: Error
}

export class ErrorShow extends React.Component<ErrorShowProps, undefined>{
    render() {
        return <MonacoWrapper
            language="json"
            width={window.innerWidth}
            height={window.innerHeight - 50}
            value={JSON.stringify(this.props.error, null, 4)}
        />
    }
}