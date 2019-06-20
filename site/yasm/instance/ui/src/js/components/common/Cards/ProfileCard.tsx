import * as React from "react";
import {PersonCard} from "./PersonCard";
import {connect} from "react-redux";
import {faSignInAlt, faSignOutAlt} from "@fortawesome/free-solid-svg-icons";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {Person} from "../../../generated/interfaces";
import {loadProfileOnce} from "../../../redux-structure/api-calls/profile";

interface ProfileCardProps {
    profile?: Person,
    dispatch?: (action: any) => void,
}

@(connect((state: any) => {
    return {profile: state.PROFILE}
}) as any)
export class ProfileCard extends React.Component<ProfileCardProps> {
    componentWillMount(): void {
        loadProfileOnce(this.props.dispatch);
    }

    render() {
        if (this.props.profile) {
            return (
                <PersonCard person={this.props.profile}/>
            )
        } else {
            return null
        }
    }
}
