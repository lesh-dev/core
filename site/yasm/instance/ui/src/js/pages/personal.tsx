import * as React from "react";
import * as ReactDOM from "react-dom";
import {BrowserRouter} from "react-router-dom";
import {Person} from "../generated/interfaces";
import {get_profile} from "../api/personal"
import {Spinner} from "../components/common/Spinner";
import {Contacts} from "../components/common/Lists/Contacts";

interface PersonalState {
    person: Person
}

class Personal extends React.Component<undefined, PersonalState> {
    constructor(props: any) {
        super(props);
        get_profile().then(
            value => this.setState({person: value})
        )
    }

    render() {
        if (this.state && false) {
            return <div>
                <Contacts person={this.state.person}/>
            </div>
        } else {
            return <Spinner/>
        }
    }
}


ReactDOM.render((
    <Personal/>
), document.getElementById('mount-point'));
