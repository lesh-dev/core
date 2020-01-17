import * as React from "react";
import {connect} from "react-redux";
import {ReduxProps} from "../../redux-structure/store";
import {MonacoWrapper, Spinner} from "../../components/common";
import {commonActions, CommonState} from "../../redux-structure/common";
import {BigAva} from "../../components/internal/BigAva";
import {Contacts} from "../../components/internal/Contacts";
import {PersonalParams} from "./params";
import {RouterProps} from "../../util/match";
import {internalActions, InternalState} from "../../redux-structure/internal";

@(connect((state: any) => state) as any)
export class Personal extends React.Component<{common?: CommonState, internal?: InternalState} & ReduxProps & RouterProps<PersonalParams>> {
    self = false
    componentDidMount(): void {

        const id = Number((this.props.match || {params: {id: this.props.common.login.profile.person_id}}).params.id)
        this.self = this.props.common.login.profile.person_id === id
        if (this.self) {
            this.props.dispatch(commonActions.common.login.fetch(false))
        } else {
            this.props.dispatch(internalActions.internal.person.fetch(id))
        }
    }

    render(): React.ReactNode {
        const state = this.self ? this.props.common.login : this.props.internal.person
        if (state.error !== undefined) {
            return <>
                <MonacoWrapper
                    language="json"
                    width={window.innerWidth}
                    height={window.innerHeight - 50}
                    value={JSON.stringify(state.error, null, 4)}
                />
            </>
        }
        if (state.loading || state.profile === undefined) {
            return <Spinner/>
        }
        return <>
            <BigAva person={state.profile}/>
            <Contacts person={state.profile}/>
        </>
    }
}
