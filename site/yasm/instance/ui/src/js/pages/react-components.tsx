import * as React from "react";
import * as ReactDOM from "react-dom";
import {Spinner} from "../components/common/Spinner";
import {Route, Router, Switch} from "react-router";
import {BrowserRouter, Link} from "react-router-dom";
import {Cut, CutProps} from "../components/common/Cut";
import {ET} from "../components/common/EditableText";
import {PersonCard} from "../components/common/Cards/PersonCard";
import {SchoolCard} from "../components/common/Cards/SchoolCard";
import {SideMenu} from "../components/common/SideMenu";
import {default_Contact, default_Course, default_Person, default_School} from "../generated/defaults";
import {CourseCard} from "../components/common/Cards/CourseCard";
import {ContactCard} from "../components/common/Cards/ContactCard";

let loremIpsum = require("lorem-ipsum");


const Main = () => (
    <main style={{
        flexGrow: 1,
        borderColor: "gray",
        borderWidth: "1px",
        borderStyle: "solid",
        padding: "5px",
    }}>
        <Switch>
            <Route exact
                   path='/RC/spinner'
                   component={Spinner}/>
            <Route exact
                   path='/RC/cut'
                   render={() => <Cut content={
                       <div>
                           {loremIpsum()}
                       </div>
                   } label={"Label"}/>}/>
            <Route exact
                   path='/RC/editable_text'
                   render={() => <ET text={loremIpsum()} callback={(v: any) => {
                       console.log("callback with v:", v)
                   }}/>}/>
            <Route exact
                   path='/RC/side_menu' render={() => <SideMenu entries={[
                {
                    url: "ya.ru",
                    label: "YandeX"
                },
                {
                    label: "test",
                    subentries: [
                        {
                            label: "A",
                            url: "ya.ru"
                        },
                        {
                            label: "B",
                            subentries: [
                                {
                                    label: "C",
                                    url: "ya.ru"
                                }
                            ]
                        }
                    ]
                }
            ]}/>}/>
            <Route exact
                   path='/RC/person_card'
                   render={() => {
                       return <PersonCard person={default_Person}/>;
                   }}/>
            <Route exact
                   path='/RC/school_card'
                   render={() => <SchoolCard school={default_School}/>}/>
            <Route exact
                   path='/RC/course_card'
                   render={() => <CourseCard course={default_Course}/>}/>
            <Route exact
                   path='/RC/contact_card'
                   render={() => <ContactCard contact={default_Contact}/>} />
        </Switch>
    </main>
);


const Header = () => (
    <header>
        <nav>
            <ul>
                <li><Link to='/RC/spinner'>Spinner</Link></li>
                <li><Link to='/RC/cut'>Cut</Link></li>
                <li><Link to={'/RC/editable_text'}>EditableText</Link></li>
                <li><Link to={'/RC/side_menu'}>SideMenu</Link></li>
                <li><Link to={'/RC/person_card'}>PersonCard</Link></li>
                <li><Link to={'/RC/school_card'}>SchoolCard</Link></li>
                <li><Link to={'/RC/course_card'}>CourseCard</Link></li>
                <li><Link to={'/RC/contact_card'}>ContactCard</Link></li>
            </ul>
        </nav>
    </header>
);

const App = () => (
    <div style={{display: "flex", justifyContent: "space-between"}}>
        <Header/>
        <Main/>
    </div>
);


ReactDOM.render((
    <BrowserRouter>
        <App/>
    </BrowserRouter>
), document.getElementById('mount-point'));
