import * as React from "react";
import {connect} from "react-redux";
import {ReduxProps} from "../../redux-structure/store";
import {MonacoWrapper, Spinner} from "../../components/common";
import {CommonState} from "../../redux-structure/common";
import {Link} from "react-router-dom";


@(connect((state: any) => state.common) as any)
export class Personal extends React.Component<CommonState & ReduxProps> {
    render(): React.ReactNode {
        if (this.props.login.error !== undefined) {
            return <>
                <MonacoWrapper
                    language="json"
                    width={window.innerWidth}
                    height={window.innerHeight - 50}
                    value={JSON.stringify(this.props.login.error, null, 4)}
                />
            </>
        }
        if (this.props.login.loading) {
            return <Spinner/>
        }
        return (
            <Link to={'/i/courses'}>Мои Курсы</Link>
        )
    }
}
