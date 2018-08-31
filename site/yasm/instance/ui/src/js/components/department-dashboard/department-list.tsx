import * as React from "react";
import {Department, DepartmentList} from "../../generated/interfaces";
import {department_list} from "../../generated/api_connect";
import {Spinner} from "../common/Spinner";
import {DepartmentCard} from "../common/DepartmentCard";
import Async from "react-promise";
import {List} from "../common/List";


export class DepsList extends React.Component {
    render() {
        return <Async promise={department_list()}
                      then={(list: DepartmentList) => {
                          return <List renderer={(department: Department) => {
                              return <DepartmentCard department={department}
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