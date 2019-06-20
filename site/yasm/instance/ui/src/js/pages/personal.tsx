import * as React from "react";
import * as ReactDOM from "react-dom";
import {Person} from "../generated/interfaces";
import {BasePage} from "./base";
import {connect} from "react-redux";
import {loadProfileOnce} from "../redux-structure/api-calls/profile";


interface PersonalProps {
    dispatch?: (action: any) => void,
    profile?: Person,
}

@(connect((state: any) => {return {profile: state.PROFILE}}) as any)
class Personal extends React.Component<PersonalProps> {
    constructor(props: PersonalProps) {
        super(props);
    }

    componentWillMount(): void {
        loadProfileOnce(this.props.dispatch);
    }

    render(): React.ReactNode {
        console.log(this.props);
        return this.props.profile ? this.props.profile.rights : 'WASP'
    }
}


ReactDOM.render((
    <BasePage
        page_renderer={() => <Personal/>}
    />
), document.getElementById('mount-point'));
