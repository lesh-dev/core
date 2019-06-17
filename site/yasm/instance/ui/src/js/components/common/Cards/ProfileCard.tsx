import * as React from "react";
import {PersonCard} from "./PersonCard";
import {connect} from "react-redux";
import {faSignInAlt, faSignOutAlt} from "@fortawesome/free-solid-svg-icons";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";

@(connect((state: any) => state.PROFILE) as any)
export class ProfileCard extends React.Component {
    render() {
        if (this.props) {
            return (
                <React.Fragment>
                    <PersonCard person={this.props as any}/>
                    <FontAwesomeIcon icon={faSignOutAlt}/>
                </React.Fragment>
            )
        } else {
            return (
                <React.Fragment>
                    <FontAwesomeIcon icon={faSignInAlt}/>
                </React.Fragment>
            )
        }
    }
}
