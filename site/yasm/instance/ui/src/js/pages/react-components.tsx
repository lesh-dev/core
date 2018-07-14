import * as React from "react";
import * as ReactDOM from "react-dom";
import {Spinner} from "../components/common/Spinner";
import {Route, Router, Switch} from "react-router";
import {BrowserRouter, Link} from "react-router-dom";
import {Cut, CutProps} from "../components/common/Cut";
import {ET} from "../components/common/EditableText";
import {PersonCard} from "../components/common/PersonCard";
import {SchoolCard} from "../components/common/SchoolCard";
import {SideMenu} from "../components/common/SideMenu";

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
                   path='/RC/person_card'
                   render={() => <PersonCard nick="rebenkoy"
                                             name="Ребенко Ярослав"
                                             img={"https://pp.userapi.com/c637326/v637326823/30fa3/JdGgrv7ZMxo.jpg?ava=1"}
                                             callback={() => console.log(loremIpsum())}/>}/>
            <Route exac
                   path='/RC/school_card'
                   render={() => <SchoolCard title={"The School"}
                                             dates={"never-now"}
                                             place={"neverland"}
                                             emblem={"https://s.hdnux.com/photos/53/27/02/11366561/5/920x920.jpg"}/>}/>
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
                <li><Link to={'/RC/person_card'}>PersonCard</Link></li>
                <li><Link to={'/RC/school_card'}>SchoolCard</Link></li>
                <li><Link to={'/RC/side_menu'}>SideMenu</Link></li>
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
