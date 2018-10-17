import * as React from "react";
import * as ReactDOM from "react-dom";
import {BrowserRouter} from "react-router-dom";
import {Person} from "../generated/interfaces";
import {get_profile} from "../api/personal"
import {PersonCard} from "../components/common/Cards/PersonCard";
import {Spinner} from "../components/common/Spinner";

interface PersonalState {
    person: Person
}

class Personal extends React.Component<undefined, PersonalState> {
    constructor(props: any) {
        super(props);
        get_profile().then(result => this.setState({person: result}), error => console.log(error))
    }
    render() {
        if (this.state) {
            return <PersonCard person={this.state.person}/>
        } else {
            return <Spinner/>
        }
    }
}


ReactDOM.render((
    <BrowserRouter>
        <Personal/>
    </BrowserRouter>
), document.getElementById('mount-point'));