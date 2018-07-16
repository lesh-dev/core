import * as React from "react";
import {School, SchoolList} from "../../generated/interfaces";
import {school_list} from "../../generated/api_connect";
import {Spinner} from "../common/Spinner";
import {SchoolCard} from "../common/SchoolCard";
import Async from "react-promise";
import {List} from "../common/List";


export class SchList extends React.Component {
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
                          }} data={list.values}/>
                      }
                      }
                      pending={() => <Spinner/>}/>;
    }
}

// import * as React from "react";
// import {School, SchoolList} from "../../generated/interfaces";
// import {callbackify} from "util";
// import {SchoolCard} from "../common/SchoolCard";
// import {school_list} from "../../generated/api_connect";
// import {Spinner} from "../common/Spinner";
// import '../../../scss/school.scss'
// import {redirect} from "../common/utils";
//
//
// interface SLEntryProps {
//     sch: School
//     callback: () => void
// }
//
// class SLEntry extends React.Component<SLEntryProps> {
//     render() {
//         return <div onClick={() => this.props.callback()}>{this.props.sch.school_title}</div>
//     }
//
// }
//
// export interface SchListProps {
//     prefix?: string
// }
//
// interface SchListState {
//     sch_list: SchoolList
// }
//
//
// export class SchList extends React.Component<SchListProps, SchListState> {
//     constructor(props: any) {
//         super(props);
//         school_list().then((value: SchoolList) => {
//             this.setState({sch_list: value})
//         })
//     }
//     render_list() {
//         let ans = [];
//         for (let i = this.state.sch_list.length - 1; i >= 0; --i) {
//             ans.push(<SchoolCard school={this.state.sch_list.values[i]}
//                                  callback={() => {this.choose(i)}}
//                                  style={{
//                                      display: "flex",
//                                      justifyContent: "left"
//                                  }}/>);
//         }
//         return ans;
//     }
//
//     choose(i: number) {
//         redirect(this.props.prefix + '/' + this.state.sch_list.values[i].school_id)
//     }
//
//     render() {
//         return (this.state) ? <div className="list">
//             {this.render_list()}
//         </div> : <Spinner/>
//     }
// }