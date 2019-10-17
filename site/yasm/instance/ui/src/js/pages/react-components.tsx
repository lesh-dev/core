import * as React from "react";
import * as ReactDOM from "react-dom";
import {Spinner} from "../components/common/Spinner";
import {Route, Switch} from "react-router";
import {BrowserRouter, Link} from "react-router-dom";
import {Cut} from "../components/common/Cut";
import {ET} from "../components/common/EditableText";
import {SideMenu} from "../components/common/SideMenu";
import {SearchPresentation, default_SearchExample, SearchExample} from "../components/common/Search"
import {TestHighlight} from "../components/common/Snippet";
import {ExamsExample} from "../components/common/Exams"
import {CalendarExample} from "../components/common/Calendar";
import {ATExample} from "../components/common/Attributes";

import loremIpsum = require("lorem-ipsum");
import {LoginForm} from "../components/forms/login";
import {LoginPocket} from  '../components/common/LoginPocket';
import {Dropdown} from "../components/common/Dropdown";
import {BasePage} from "./base";
import {Table} from "../components/common/Table";
import {Example} from "../components/common/Example";


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
                   path='/RC/search_presentation'
                   render={() => <SearchPresentation result={default_SearchExample} query={'й а'}
                                                     onQueryChange={q => console.log("query", q)}/>}/>
            <Route exact
                   path='/RC/search_example'
                   render={() => <SearchExample/>}/>
            <Route exact
                   path='/RC/snippet'
                   render={() => <TestHighlight/>}/>
            <Route exact
                   path='/RC/exams'
                   render={ExamsExample}/>
            <Route exact
                   path='/RC/calendar'
                   render={() => <CalendarExample/>}/>
            <Route exact
                   path='/RC/attributes'
                   render={() => <ATExample/>}/>
            <Route exact
                   path='/RC/loginform'
                   render={() => <LoginForm/>}/>
            <Route exact
                   path='/RC/loginpocket'
                   render={() => <LoginPocket/>}/>
            <Route exact
                   path='/RC/dropdown-click'
                   render={() => <Dropdown
                       label={() => <div className='test'>ASD</div>}
                       component={() => <React.Fragment><div>ASD1</div><div>ASD2</div></React.Fragment>}
                       onCollapse={() => console.log('collapsed')}
                       onExpand={() => console.log('expanded')}
                   />
                   }/>
            <Route exact
                   path='/RC/dropdown-hover'
                   render={() => <Example
                       fields={[
                           {
                               name: 'type',
                               type: 'choice',
                               choices: ['hover', 'click'],
                               default: 'hover'
                           },
                           {
                               name: 'label',
                               type: 'function',
                               default: () => <div className='test'>ASD</div>
                           },
                           {
                               name: 'component',
                               type: 'function',
                               default: () => <React.Fragment><div>ASD1</div><div>ASD2</div></React.Fragment>
                           },
                           {
                               name: 'onCollapse',
                               type: 'function',
                               default: () => console.log('collapsed')
                           },
                           {
                               name: 'onExpand',
                               type: 'function',
                               default: () => console.log('expanded')
                           }
                       ]}
                       renderer={props => <Dropdown
                           {...props}
                       />}
                   />}
            />
            <Route exact
                   path='/RC/table'
                   render={() =>
                       <Example
                           fields={
                               [
                                   {
                                       name: 'header',
                                       type: 'object',
                                       default: `
{
    "columns": [
        {
            "value": "A"
        },
        {
            "value": "B",
            "title": "b"
        },
        {
            "value": "C",
            "groupable": true
        },
        {
            "value": "D",
            "sortable": true
        },
        {
            "value": "E",
            "sortable": true,
            "groupable": true
        }
    ]
}`
                                   },
                                   {
                                       type: 'JSON',
                                       name: 'content',
                                       default: `
[
    {
        "A": 1,
        "B": 2,
        "C": 3,
        "D": 4,
        "E": 5
    },
    {
        "A": 10,
        "B": 20,
        "C": 2,
        "D": 40,
        "E": 5
    },
    {
        "A": 12,
        "B": 22,
        "C": 3,
        "D": 3,
        "E": 4
    }
]`
                                   }
                               ]
                           }
                           renderer={props =>
                               <Table
                                   {...props}
                               />
                           }
                       />
                   }
               />
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
                <li><Link to={'/RC/snippet'}>Snippet</Link></li>
                <li><Link to={'/RC/search_presentation'}>SearchPresentation</Link></li>
                <li><Link to={'/RC/search_example'}>SearchExample (live)</Link></li>
                <li><Link to={'/RC/exams'}>Exams (live)</Link></li>
                <li><Link to={'/RC/calendar'}>Calendar </Link></li>
                <li><Link to={'/RC/attributes'}>Attribute Table</Link></li>
                <li><Link to={'/RC/loginform'}>Login Form</Link></li>
                <li><Link to={'/RC/loginpocket'}>Login Pocket</Link></li>
                <li><Link to={'/RC/dropdown-click'}>Dropdown click</Link></li>
                <li><Link to={'/RC/dropdown-hover'}>Dropdown hover</Link></li>
                <li><Link to={'/RC/table'}>Table</Link></li>
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
        <BasePage page_renderer={() => <App/>}/>
    </BrowserRouter>
), document.getElementById('mount-point'));
