import * as React from "react"
import {connect, Provider, Store} from "react-redux"
import {applyMiddleware, createStore} from "redux"
import thunkMiddleware from 'redux-thunk'
import { createLogger } from 'redux-logger'
import { composeWithDevTools } from 'redux-devtools-extension'
import {Snippet, HighlightTitle} from "./Snippet"

// ____ _____  _  _____ _____
// / ___|_   _|/ \|_   _| ____|
// \___ \ | | / _ \ | | |  _|
// ___) | | |/ ___ \| | | |___
// |____/ |_/_/   \_\_| |_____|
//

export interface SearchResultItem {
    source: string,
    id: number,
    title: string,
    description: string
}

export interface SearchResult {
    result: SearchResultItem[]
}

export interface SearchProps {
    result: SearchResultItem[]
    query: string
    onQueryChange: (query: string) => void
}

export interface SearchStateShape {
    result: SearchResultItem[]
    query: string
    status: "ready" | "pending"
}

const initialState: SearchStateShape = {
    result: [],
    query: "",
    status: "ready",
};


// ____  ____  _____ ____  _____ _   _ _____  _  _____ ___ ___  _   _
// |  _ \|  _ \| ____/ ___|| ____| \ | |_   _|/ \|_   _|_ _/ _ \| \ | |
// | |_) | |_) |  _| \___ \|  _| |  \| | | | / _ \ | |  | | | | |  \| |
// |  __/|  _ <| |___ ___) | |___| |\  | | |/ ___ \| |  | | |_| | |\  |
// |_|   |_| \_\_____|____/|_____|_| \_| |_/_/   \_\_| |___\___/|_| \_|
//

export class SearchBar extends React.Component<{onQueryChange: (query: string) => void, query: string}> {
    render() {
        return <input type="text" placeholder="search" value={this.props.query} onChange={e => this.props.onQueryChange(e.target.value)}/>
    }
}


const makeLink = (row: SearchResultItem) => {
    switch(row.source) {
        case "person":
            return `/admin/gui/people/${row.id}`;
        case "course":
            return `/admin/gui/course/${row.id}`;
        default:
            return `/admin/gui/404/${row.id}`
    }
};

export class SearchResultRow extends React.Component<SearchResultItem & { query: string }> {
    render() {
        return (<div>
            <span style={{fontSize: "0.6em", verticalAlign: "center", color: "grey"}}>
                { this.props.source }:
            </span>
            {' '}
            <a href={makeLink(this.props)} children={ HighlightTitle(this.props) }/>
            <Snippet query={this.props.query} stopwords={this.props.title} content={this.props.description} />
        </div>);
    }
}

export class SearchStatic extends React.Component<SearchProps> {
    render() {
        return (<div>
            <SearchBar query={this.props.query} onQueryChange={this.props.onQueryChange}/>
            { this.props.result.map((r) =>
                <SearchResultRow key={r.source + ' ' + r.id} {...r} query={this.props.query}/>)}
        </div>);
    }
}


//    _    ____ _____ ___ ___  _   _ ____
//    / \  / ___|_   _|_ _/ _ \| \ | / ___|
//   / _ \| |     | |  | | | | |  \| \___ \
//  / ___ \ |___  | |  | | |_| | |\  |___) |
// /_/   \_\____| |_| |___\___/|_| \_|____/
//

const SEARCH_REQUEST = "SEARCH_REQUEST";
const searchRequest = (query: string) => ({ type: SEARCH_REQUEST, query });

const SEARCH_RESPONSE = "SEARCH_RESPONSE";
const searchResponse = (result: SearchResultItem[], query: string) =>
    ({ type: SEARCH_RESPONSE, result, query });


// ____  _____ ____  _   _  ____ _____ ____  ____
// |  _ \| ____|  _ \| | | |/ ___| ____|  _ \/ ___|
// | |_) |  _| | | | | | | | |   |  _| | |_) \___ \
// |  _ <| |___| |_| | |_| | |___| |___|  _ < ___) |
// |_| \_\_____|____/ \___/ \____|_____|_| \_\____/
//

function app(state = initialState, action: any) {
    switch(action.type) {
        case SEARCH_RESPONSE:
            if(state.query === action.query) {
                return Object.assign({}, state, {
                    status: "ready",
                    result: action.result
                });
            } else return state; // запрос устарел, результат потерял актуальность

        case SEARCH_REQUEST:
            return Object.assign({}, state, {
                status: "pending",
                query: action.query
            });
        default:
            return state;
    }
}

// ____ _____ ___  ____  _____
// / ___|_   _/ _ \|  _ \| ____|
// \___ \ | || | | | |_) |  _|
// ___) | | || |_| |  _ <| |___
// |____/ |_| \___/|_| \_\_____|
//

export const makeStore = () => createStore(app, composeWithDevTools( applyMiddleware(thunkMiddleware, createLogger()) ));

//   ____ ___  _   _ _____  _    ___ _   _ _____ ____  ____
//  / ___/ _ \| \ | |_   _|/ \  |_ _| \ | | ____|  _ \/ ___|
// | |  | | | |  \| | | | / _ \  | ||  \| |  _| | |_) \___ \
// | |__| |_| | |\  | | |/ ___ \ | || |\  | |___|  _ < ___) |
//  \____\___/|_| \_| |_/_/   \_\___|_| \_|_____|_| \_\____/
//

const mapStateToProps = (state: SearchStateShape) => ({
    result: state.result,
    query: state.query
});

/// Мы могли бы использовать plain версию...
// const mapDispatchToProps = (dispatch: any) => ({
//     onQueryChange: (query: string) => {
//         dispatch(searchRequest(query));
//         const baseUri = "//127.0.0.1:3000/search?";
//         const uri = baseUri + "limit=5&description=" + encodeURIComponent(`ilike.%${query}%`);
//         fetch(uri)
//             .then(resp => resp.json())
//             .then(j => dispatch(searchResponse(j)) )
//     }
// });


// ... Но thunk позволяет получить состояние, из которого нам могут понадобиться статус и результаты setTimeout
const mapDispatchToProps = ({
    onQueryChange: (query: string) => (dispatch: (action: any) => void, getState: () => any) => {
        if(query.trim() == '') {
            dispatch(searchRequest(query));
            dispatch(searchResponse([], query));
            return;
        } // empty string => don't search
        dispatch(searchRequest(query));
        console.log("state.status", getState().status); // demonstration
        const baseUri = "//127.0.0.1:3000/search?";
        const terms = query.split(/\s+/);
        //const uri = baseUri + "limit=5&description=" + encodeURIComponent(`ilike.%${query}%`);
        const clauses = terms.map(t => '&description=ilike.' + encodeURIComponent(`%${t}%`));
        const uri = baseUri + "limit=5" + clauses.join('');
        fetch(uri)
            .then(resp => resp.json())
            .then(j => dispatch(searchResponse(j, query)) )
        // todo: handle errors
    }
});


export const Search = connect(mapStateToProps, mapDispatchToProps)(
    ({ result, onQueryChange, query}) => <SearchStatic result={result} onQueryChange={onQueryChange} query={query} />
);


//  _______  __    _    __  __ ____  _     _____ ____
// | ____\ \/ /   / \  |  \/  |  _ \| |   | ____/ ___|
// |  _|  \  /   / _ \ | |\/| | |_) | |   |  _| \___ \
// | |___ /  \  / ___ \| |  | |  __/| |___| |___ ___) |
// |_____/_/\_\/_/   \_\_|  |_|_|   |_____|_____|____/
//

export const default_SearchExample =
    [{"source":"person","id":705,"title":"Аэлина Габидуллина","description":"Аэлина Айратовна Габидуллина  Aelinagabidullna@gmail.com  "},
    {"source":"person","id":372,"title":"Алексей Сульгин","description":"Алексей Андреевич Сульгин    "},
    {"source":"course","id":302,"title":"Математический анализ-2","description":"Математический анализ-2 "},
    {"source":"person","id":840,"title":"Айдамир Гучетль","description":"Айдамир Юрьевич Гучетль  guchetl0745@icloud.com  "},
    {"source":"person","id":829,"title":"Анастасия Коновалова","description":"Анастасия Михайловна Коновалова  cat_kon@mail.ru  "}]

export class SearchExample extends React.Component<any> {
    constructor(props: any){
        super(props);
        this.store = makeStore();
    }
    store: Store<SearchStateShape>;

    render() {
        return <Provider store={this.store}><Search/></Provider>
    }
}
