import * as React from "react";
import {connect} from "react-redux";
import {ReduxProps} from "../../redux-structure/store";
import {CommonState} from "../../redux-structure/common";
import {PersonalParams} from "./params";
import {RouterProps} from "../../util/match";
import {internalActions, InternalState} from "../../redux-structure/internal";
import {ErrorShow} from "../../components/common/ErrorShow";
import {Spinner} from "../../components/common";
import {Teachers} from "../../components/internal/course/Teachers";

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
        if (this.props.internal.course.error !== undefined) {
            return <ErrorShow error={this.props.internal.course.error}/>
        }
        if (this.props.internal.course.loading || this.props.internal.course.course === undefined) {
            return <Spinner/>
        }
        return <>
            {
                this.props.internal.course.course.title
            }
        <Teachers/>
        </>
    }
}
