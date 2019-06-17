import * as React from "react";
import * as ReactDOM from "react-dom";
import {Person} from "../generated/interfaces";
import {get_profile} from "../api/personal"
import {BasePage} from "./base";
import {connect} from "react-redux";
import {profileReducer} from "./reducers/personal";
import {profileLoaded} from "./actions/personal";
import {Spinner} from "../components/common/Spinner";


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
        get_profile().then(value => {
            this.props.dispatch(profileLoaded(value));
        })
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
