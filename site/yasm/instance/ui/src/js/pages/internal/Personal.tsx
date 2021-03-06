import * as React from "react";
import {connect} from "react-redux";
import {ReduxProps} from "../../redux-structure/store";
import {MonacoWrapper, Spinner} from "../../components/common";
import {commonActions, CommonState} from "../../redux-structure/common";
import {BigAva} from "../../components/internal/personal/BigAva";
import {Contacts} from "../../components/internal/personal/Contacts";
import {PersonalParams} from "./params";
import {RouterProps} from "../../util/match";
import {internalActions, InternalState} from "../../redux-structure/internal";
import {ErrorShow} from "../../components/common/ErrorShow";
import {ReduxAutofireAction} from "../../components/reduxAutofireAction";

@(connect((state: any) => state) as any)
export class Personal extends ReduxAutofireAction<{common?: CommonState, internal?: InternalState} & ReduxProps & RouterProps<PersonalParams>> {
    self = false
    id = 0
    mounted = false

    constructor(props: any, ctx: any) {
        super(props, ctx);
        this.update = this.update.bind(this)
    }

    reload_should(): boolean {
        return super.reload_should() && this.mounted;
    }

    reload(initial=false) {
        if (initial) {
            this.self = this.props.common.login.profile.id === this.id
            if (this.self) {
                this.props.dispatch(commonActions.common.login.fetchInit(false))
            } else {
                this.props.dispatch(internalActions.internal.person.fetchInit(this.id))
            }
        } else {
            this.self = this.props.common.login.profile.id === this.id
            if (this.self) {
                this.props.dispatch(commonActions.common.login.fetch(false))
            } else {
                this.props.dispatch(internalActions.internal.person.fetch(this.id))
            }
        }
    }

    private update() {
        const id = Number((this.props.match || {params: {id: this.props.common.login.profile.id}}).params.id)
        if (id !== this.id) {
            this.id = id
            this.reload(true)
        }
    }

    componentDidMount(): void {
        this.mounted = true
        this.update()
    }

    componentDidUpdate(): void {
        this.update()
    }

    render(): React.ReactNode {
        const state = this.self ? this.props.common.login : this.props.internal.person
        if (state.error !== undefined) {
            return <ErrorShow error={state.error}/>
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
