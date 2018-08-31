import * as React from "react";
import * as ReactDOM from "react-dom";
import {BrowserRouter, match, Route, Switch} from "react-router-dom";
import {SideMenu} from "../components/common/SideMenu";
import {SchList} from "../components/school-dashboard/sch_list";
import {SchoolDashboard} from "../components/school-dashboard/school-dashboard";
import {PersList} from "../components/person-dashboard/person-list";
import {PersonDashboard} from "../components/person-dashboard/person-dashboard";
import {DepsList} from "../components/department-dashboard/department-list";
import {DepartmentDashboard} from "../components/department-dashboard/department-dashboard";

const prefix = '/admin/gui';

const Main = () => (
    <Switch>
        <Route exact path={prefix + '/schools/list'} render={() =>
            <SchList/>
        }/>
        <Route exact path={prefix + '/schools/:id'} render={({match}) =>
            <SchoolDashboard sch={match.params.id}/>
        }/>
        <Route exact path={prefix + '/people/list'} render={() =>
            <PersList/>
        }/>
        <Route exact path={prefix + '/people/:id'} render={({match}) =>
            <PersonDashboard person_id={match.params.id}/>
        }/>
        <Route exact path={prefix + '/departments/list'} render={() =>
            <DepsList/>
        }/>
        <Route exact path={prefix + '/departments/:id'} render={({match}) =>
            <DepartmentDashboard department_id={match.params.id}/>
        }/>
    </Switch>
);

const App = () => (
    <div style={{display: "flex"}}>
        <SideMenu entries={[
            {
                url: prefix + '/schools/list',
                label: 'События'
            },
            {
                url: prefix + '/people/list',
                label: 'Люди'
            },
            {
                url: prefix + '/departments/list',
                label: 'Отделения'
            }
        ]}/>
        <div style={{flexGrow: 1}}><Main/></div>
    </div>
);


ReactDOM.render((
    <BrowserRouter>
        <App/>
    </BrowserRouter>
), document.getElementById('mount-point'));