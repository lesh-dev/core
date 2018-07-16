import * as React from "react";
import {Person, PersonList} from "../../generated/interfaces";
import {person_list} from "../../generated/api_connect";
import {Spinner} from "../common/Spinner";
import {PersonCard} from "../common/PersonCard";
import Async from "react-promise";
import {List} from "../common/List";


export class PersList extends React.Component {
    render() {
        return <Async promise={person_list()}
                      then={(list: PersonList) => {
                          return <List renderer={(person: Person) => {
                              return <PersonCard person={person}
                                                 style={{
                                                     display: "flex",
                                                     justifyContent: "left"
                                                 }}
                                                 clickable={true}
                              />
                          }} data={list.values}/>
                      }
                      }
                      pending={() => <Spinner/>}/>;
    }
}