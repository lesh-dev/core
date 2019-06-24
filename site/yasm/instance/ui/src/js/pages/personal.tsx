import * as React from "react";
import * as ReactDOM from "react-dom";
import {Person} from "../generated/interfaces";
import {BasePage} from "./base";
import {connect} from "react-redux";
import {loadProfileOnce, updateExams} from "../redux-structure/api-calls/profile";


interface PersonalProps {
    dispatch?: (action: any) => any,
    profile?: Person,
}

@(connect((state: any) => {
    return {profile: state.PROFILE}
}) as any)
class Personal extends React.Component<PersonalProps> {
    constructor(props: PersonalProps) {
        super(props);
    }

    componentWillMount(): void {
        this.props.dispatch(loadProfileOnce)
        this.props.dispatch(updateExams)
    }

    componentDidUpdate(nextProps: Readonly<PersonalProps>, nextState: Readonly<{}>, nextContext: any): void {

    }

    render(): React.ReactNode {
        return this.props.profile ? this.props.profile.rights : 'WASP'
    }
}


ReactDOM.render((
    <BasePage
        page_renderer={() => <Personal/>}
    />
), document.getElementById('mount-point'));
