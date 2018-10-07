import * as React from "react";
import {School, SchoolList} from "../../generated/interfaces";
import {school_list} from "../../generated/api_connect";
import {Spinner} from "../common/Spinner";
import {SchoolCard} from "../common/Cards/SchoolCard";
import Async from "react-promise";
import {List} from "../common/List";


interface SchListState {
    list: SchoolList
}


export class SchList extends React.Component<undefined, SchListState> {
    constructor(props: any) {
        super(props);
        school_list().then(
            value => {this.setState({list: value})},
            error => {console.log(error)}
            );
        document.addEventListener('keypress', (e: any) => {this.keypress(e)})
    }
    keypress(e: any) {
        console.log(e)
    }

    render() {
        if (this.state) {
            return <List renderer={(school: School) => {
                return <SchoolCard school={school}
                                   style={{
                                       display: "flex",
                                       justifyContent: "left"
                                   }}
                                   clickable={true}
                />
            }}
                         data={this.state.list.values.reverse()}
            />
        } else {
            return <Spinner/>
        }
    }
}