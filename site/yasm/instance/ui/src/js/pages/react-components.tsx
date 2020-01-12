import * as React from "react";
import * as ReactDOM from "react-dom";
import {Spinner} from "../components/common/Spinner";
import {Route, Switch} from "react-router";
import {BrowserRouter, Link} from "react-router-dom";
import {Cut} from "../components/common/Cut";
import {ET} from "../components/common/EditableText";
import {SearchPresentation, default_SearchExample, SearchExample} from "../components/common/Search"
import {TestHighlight} from "../components/common/Snippet";
import {ExamsExample} from "../components/common/Exams"
import {CalendarExample} from "../components/common/Calendar";
import {ATExample} from "../components/common/Attributes";

import loremIpsum = require("lorem-ipsum");
import {LoginForm} from "../components/forms/login";
import {LoginPocket} from '../components/common/LoginPocket';
import {Dropdown} from "../components/common/Dropdown";
import {BasePage} from "./base";
import {Table} from "../components/common/Table";
import {Example} from "../components/common/Example";
import {QuestMaster} from "../components/common/QuestMaster";

interface MenuEntry {
    url: string,
    title: string,
    render: () => React.ReactNode,
}

class App extends React.Component {
    private static menu: MenuEntry[] = [
        {
            url: 'spinner',
            title: 'Spinner',
            render: () => <Spinner/>
        },
        {
            url: 'snippet',
            title: 'Snippet',
            render: () => <TestHighlight/>
        },
        {
            url: 'search_presentation',
            title: 'SearchPresentation',
            render: () => <SearchPresentation result={default_SearchExample} query={'й а'}
                                              onQueryChange={q => console.log("query", q)}/>
        },
        {
            url: 'search_example',
            title: 'SearchExample (live)',
            render: () => <SearchExample/>
        },
        {
            url: 'exams',
            title: 'Exams (live)',
            render: ExamsExample
        },
        {
            url: 'calendar',
            title: 'Calendar ',
            render: () => <CalendarExample/>
        },
        {
            url: 'attributes',
            title: 'Attribute Table',
            render: () => <ATExample/>
        },
        {
            url: 'loginpocket',
            title: 'Login Pocket',
            render: () => <LoginPocket/>
        },
        {
            url: 'dropdown',
            title: 'Dropdown',
            render: () => <Example
                fields={[
                    {
                        name: 'type',

                        type: 'choice',

                        choices: ['hover',
                            'click'],

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

                        default: () => <React.Fragment>
                            <div>ASD1</div>
                            <div>ASD2</div>
                        </React.Fragment>
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
            />
        },
        {
            url: 'table',
            title: 'Table',
            render: () =>
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
        },
        {
            url: 'questmaster',
            title: 'QuestMaster',
            render: () => <QuestMaster/>
        }
    ]

    render() {
        return (
            <div style={{display: "flex", justifyContent: "space-between"}}>
                <header>
                    <nav>
                        <ul>
                            {
                                App.menu.map(entry =>
                                    <li><Link to={`/RC/${entry.url}`}>{entry.title}</Link></li>
                                )
                            }
                        </ul>
                    </nav>
                </header>
                <main style={{
                    flexGrow: 1,
                    borderColor: "gray",
                    borderWidth: "1px",
                    borderStyle: "solid",
                    padding: "5px",
                }}>
                    <Switch>
                        {
                            App.menu.map(entry =>
                                <Route
                                    exact
                                    path={`/RC/${entry.url}`}
                                    render={entry.render}
                                />
                            )
                        }
                    </Switch>
                </main>
            </div>
        )
    }
}

ReactDOM.render((
    <BasePage>
        <App/>
    </BasePage>
), document.getElementById('mount-point'));
