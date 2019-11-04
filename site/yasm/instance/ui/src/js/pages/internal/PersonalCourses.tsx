import * as React from "react";
import {connect} from "react-redux";
import {ReduxProps} from "../../redux-structure/store";
import {MonacoWrapper, Spinner} from "../../components/common";
import { InternalState, internalActions } from '../../redux-structure/internal'
import {CourseCard} from "../../components/common/Cards/CourseCard";


@(connect((state: any) => state.internal) as any)
export class PersonalCourses extends React.Component<InternalState & ReduxProps> {
    constructor(props: InternalState & ReduxProps) {
        super(props)
        props.dispatch(internalActions.internal.courses.fetch())
    }
    render(): React.ReactNode {
        if (this.props.courses.error !== undefined) {
            return <>
                <MonacoWrapper
                    language="json"
                    width={window.innerWidth}
                    height={window.innerHeight - 50}
                    value={JSON.stringify(this.props.courses.error, null, 4)}
                />
            </>
        }
        if (this.props.courses.loading || this.props.courses.list === undefined) {
            return <Spinner/>
        }
        return (
            <>
                {
                    this.props.courses.list.map(c => <CourseCard course={c}/>)
                }
            </>
        )
    }
}
