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
import {ErrorShow} from "../../components/common/ErrorShow";

@(connect((state: any) => state) as any)
export class PCourse extends React.Component<{common?: CommonState, internal?: InternalState} & ReduxProps & RouterProps<PersonalParams>> {
    id = 0

    private update() {
        const id = Number(this.props.match.params.id)
        if (id !== this.id) {
            this.id = id
            this.props.dispatch(internalActions.internal.course.fetch(this.id))
        }
    }

    componentDidMount(): void {
        this.update()
    }

    componentDidUpdate(): void {
        this.update()
    }

    render(): React.ReactNode {
        return null
    }
}
