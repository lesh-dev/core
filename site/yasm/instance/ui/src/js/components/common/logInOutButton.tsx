import * as React from "react";
import {connect} from "react-redux";
import {faSignInAlt, faSignOutAlt} from "@fortawesome/free-solid-svg-icons";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {Person} from "../../generated/interfaces";
import {loadProfileOnce} from "../../redux-structure/api-calls/profile";

interface LogInOutButtonProps {
    profile?: Person,
    dispatch?: (action: any) => void,
}

@(connect((state: any) => {
    return {profile: state.PROFILE}
}) as any)
export class LogInOutButton extends React.Component<LogInOutButtonProps> {
    componentWillMount(): void {
        this.props.dispatch(loadProfileOnce);
    }

    render() {
        if (this.props.profile) {
            return (
                <a href={'/login/logout'} style={{color: "black"}}>
                    <FontAwesomeIcon icon={faSignOutAlt}/>
                </a>
            )
        } else {
            return (
                <a href={'/login/'} style={{color: "black"}}>
                    <FontAwesomeIcon icon={faSignInAlt}/>
                </a>
            )
        }
    }
}
