import * as React from "react";
import * as ReactDOM from "react-dom";
import {BasePage} from "./base";
import {Route, Switch} from "react-router-dom";
import {Personal} from "./internal/Personal";
import {PersonalCourses} from "./internal/PersonalCourses";

import {faBook} from '@fortawesome/free-solid-svg-icons/faBook'
import {faHome} from "@fortawesome/free-solid-svg-icons/faHome";
import {faGraduationCap} from "@fortawesome/free-solid-svg-icons/faGraduationCap";

import {internalInitialState, internalReducer} from '../redux-structure/internal'
import {SidebarEntryType} from "../redux-structure/sidebar";
import {Sidebar} from "../components/common";
import {PCourse} from "./internal/PCourse";

class Internal extends React.Component {
    render(): React.ReactNode {
        return (
            <Switch>
                <Route
                    path="/i/"
                    exact
                    render={() => <Personal/>}
                />
                <Route
                    path="/i/courses/"
                    exact
                    render={() => <PersonalCourses/>}
                />
                <Route
                    path="/i/grades/"
                    exact
                    render={() => <PersonalCourses/>}
                />
                <Route
                    path="/i/person/:id"
                    exact
                    component={Personal}
                />
                <Route
                    path="/i/course/:id"
                    exact
                    component={PCourse}
                />
            </Switch>
        )
    }
}


ReactDOM.render((
    <BasePage
        reducerMap={internalReducer}
        initialState={{
            internal: internalInitialState,
        }}
        initialCommonState={{
            sidebar: {
                entries: [
                    {
                        type: SidebarEntryType.Link,
                        url: '/i/',
                        display: 'Домашняя',
                        image: faHome,
                    },
                    {
                        type: SidebarEntryType.Link,
                        url: '/i/courses/',
                        display: 'Курсы',
                        image: faBook,
                    },
                    {
                        type: SidebarEntryType.Link,
                        url: '/i/grades/',
                        display: 'Зачётка',
                        image: faGraduationCap,
                    },
                ]
            }
        }}
    >
        <div style={{display: 'flex'}}>
            <Sidebar/>
            <Internal/>
        </div>
    </BasePage>
), document.getElementById('mount-point'));
