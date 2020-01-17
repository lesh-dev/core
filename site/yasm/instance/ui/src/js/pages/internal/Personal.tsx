import * as React from "react";
import {connect} from "react-redux";
import {ReduxProps} from "../../redux-structure/store";
import {MonacoWrapper, Spinner} from "../../components/common";
import {commonActions, CommonState} from "../../redux-structure/common";
import {BigAva} from "../../components/internal/BigAva";
import {Contacts} from "../../components/internal/Contacts";

@(connect((state: any) => state.common) as any)
export class Personal extends React.Component<CommonState & ReduxProps> {
    componentDidMount(): void {
        this.props.dispatch(commonActions.common.login.fetch(false))
    }

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
        return <>
            <BigAva person={this.props.login.profile}/>
            <Contacts person={this.props.login.profile}/>
        </>
    }
}
