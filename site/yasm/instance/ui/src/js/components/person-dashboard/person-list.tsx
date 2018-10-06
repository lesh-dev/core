import * as React from "react";
import {Person, PersonList} from "../../generated/interfaces";
import {person_list} from "../../generated/api_connect";
import {Spinner} from "../common/Spinner";
import {PersonCard} from "../common/Cards/PersonCard";
import Async from "react-promise";
import {List} from "../common/List";


interface PersListState {
    list: PersonList
}


export class PersList extends React.Component<undefined, PersListState> {
    constructor(props: any) {
        super(props);
        person_list().then(
            value => {this.setState({list: value})},
            error => console.log(error)
        )
    }
    render() {
        if (this.state) {
            return <List renderer={(person: Person) => {
                return <PersonCard person={person}
                                 style={{
                                     display: "flex",
                                     justifyContent: "left"
                                 }}
                                 clickable={true}
                />
            }}
                         data={this.state.list.values}/>
        } else {
            return <Spinner/>
        }
    }
}