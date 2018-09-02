import * as React from "react";
import {School, SchoolList} from "../../generated/interfaces";
import {school_list} from "../../generated/api_connect";
import {Spinner} from "../common/Spinner";
import {SchoolCard} from "../common/SchoolCard";
import Async from "react-promise";
import {List} from "../common/List";


export class SchList extends React.Component {
    keypress(e: any) {
        console.log(e)
    }

    constructor(props: any) {
        super(props);
        document.addEventListener('keypress', (e: any) => {this.keypress(e)})
    }
    render() {
        return <Async promise={school_list()}
                      then={(list: SchoolList) => {
                          return <List renderer={(school: School) => {
                              return <SchoolCard school={school}
                                                 style={{
                                                     display: "flex",
                                                     justifyContent: "left"
                                                 }}
                                                 clickable={true}
                              />
                          }} data={list.values.reverse()}

                          />
                      }
                      }
                      pending={() => <Spinner/>}/>;
    }
}