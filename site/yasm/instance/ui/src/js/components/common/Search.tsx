import * as React from "react"
import {connect, Provider, Store} from "react-redux"
import {applyMiddleware, combineReducers, createStore} from "redux"
import thunkMiddleware from 'redux-thunk'
import { createLogger } from 'redux-logger'
import { composeWithDevTools } from 'redux-devtools-extension'
import {Snippet, HighlightTitle} from "./Snippet"
import "../../../scss/search.scss"

//  ____ _____  _  _____ _____
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


//  ____  ____  _____ ____  _____ _   _ _____  _  _____ ___ ___  _   _
// |  _ \|  _ \| ____/ ___|| ____| \ | |_   _|/ \|_   _|_ _/ _ \| \ | |
// | |_) | |_) |  _| \___ \|  _| |  \| | | | / _ \ | |  | | | | |  \| |
// |  __/|  _ <| |___ ___) | |___| |\  | | |/ ___ \| |  | | |_| | |\  |
// |_|   |_| \_\_____|____/|_____|_| \_| |_/_/   \_\_| |___\___/|_| \_|
//

export class SearchBar extends React.Component<{onQueryChange: (query: string) => void, query: string}> {
    render() {
        return <input type="text"
                      placeholder="search"
                      value={this.props.query}
                      onChange={e => this.props.onQueryChange(e.target.value)}
                      className={"search__input"}
        />
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
        return (<div className={"search__result-row"}>
            <span className={"search__result-source"}>
                { this.props.source }:
            </span>
            {' '}
            <a href={makeLink(this.props)}
               children={ HighlightTitle(this.props) }
               className={"search__result-link"}/>
            <Snippet query={this.props.query} stopwords={this.props.title} content={this.props.description} />
        </div>);
    }
}

export class SearchPresentation extends React.Component<SearchProps> {
    render() {
        return (<div className={"search"}>
            <SearchBar query={this.props.query} onQueryChange={this.props.onQueryChange}/>
            { this.props.result.map((r) =>
                <SearchResultRow key={r.source + ' ' + r.id} {...r} query={this.props.query}/>)}
        </div>);
    }
}


//     _    ____ _____ ___ ___  _   _ ____
//    / \  / ___|_   _|_ _/ _ \| \ | / ___|
//   / _ \| |     | |  | | | | |  \| \___ \
//  / ___ \ |___  | |  | | |_| | |\  |___) |
// /_/   \_\____| |_| |___\___/|_| \_|____/
//

const SEARCH_REQUEST = "SEARCH_REQUEST";
const searchRequest = (query: string, path: string[]) => ({ type: SEARCH_REQUEST, query, path });

const SEARCH_RESPONSE = "SEARCH_RESPONSE";
const searchResponse = (result: SearchResultItem[], query: string, path: string[]) =>
    ({ type: SEARCH_RESPONSE, result, query, path });


//  ____  _____ ____  _   _  ____ _____ ____  ____
// |  _ \| ____|  _ \| | | |/ ___| ____|  _ \/ ___|
// | |_) |  _| | | | | | | | |   |  _| | |_) \___ \
// |  _ <| |___| |_| | |_| | |___| |___|  _ < ___) |
// |_| \_\_____|____/ \___/ \____|_____|_| \_\____/
//

function searchReducer(state = {}, action: any) {
    switch(action.type) {
        case SEARCH_RESPONSE: {
            let query = Lens.get(state, action.path, initialState).query;
            if (query === action.query) {
                return Lens.set(state, {
                    status: "ready",
                    result: action.result
                }, action.path);
            } else return state; // запрос устарел, результат потерял актуальность
        }

        case SEARCH_REQUEST: {
            return Lens.localUpdate(state, {
                status: 'pending',
                query: action. query
            }, action.path, initialState);
        }
        default:
            return state;
    }
}

//  ____ _____ ___  ____  _____
// / ___|_   _/ _ \|  _ \| ____|
// \___ \ | || | | | |_) |  _|
// ___) | | || |_| |  _ <| |___
// |____/ |_| \___/|_| \_\_____|
//

const app = combineReducers({ search: searchReducer });
export const makeStore = () => createStore(searchReducer, composeWithDevTools( applyMiddleware(thunkMiddleware, createLogger()) ));

//   ____ ___  _   _ _____  _    ___ _   _ _____ ____  ____
//  / ___/ _ \| \ | |_   _|/ \  |_ _| \ | | ____|  _ \/ ___|
// | |  | | | |  \| | | | / _ \  | ||  \| |  _| | |_) \___ \
// | |__| |_| | |\  | | |/ ___ \ | || |\  | |___|  _ < ___) |
//  \____\___/|_| \_| |_/_/   \_\___|_| \_|_____|_| \_\____/
//

const mapStateToProps = (state: any, ownProps: { path: string[] }) => {
    const localState = Lens.get(state, ownProps.path, initialState);
    return {
        result: localState.result,
        query: localState.query
    }
};

const mapDispatchToProps = (dispatch: (action: any) => void, ownProps: { path: string[] }) => ({
    onQueryChange: (query: string) => {
        const path = ownProps.path;
        if(query.trim() == '') { // empty string => don't search
            dispatch(searchRequest(query, path));
            dispatch(searchResponse([], query, path));
            return;
        }
        dispatch(searchRequest(query, path));
        const baseUri = "//127.0.0.1:3000/search?";
        const terms = query.split(/\s+/);
        const clauses = terms.map(t => '&description=ilike.' + encodeURIComponent(`%${t}%`));
        const uri = baseUri + "limit=5" + clauses.join('');
        fetch(uri)
            .then(resp => resp.json())
            .then(j => dispatch(searchResponse(j, query, path)) )
        // todo: handle errors
    }
});

// ... Thunk позволяет получить состояние, из которого нам могут понадобиться статус и результаты setTimeout
// Но при этом не получается получить путь в дереве состояния.
const mapDispatchToPropsBroken = ({
    onQueryChange: (query: string) => (dispatch: (action: any) => void, getState: () => any, ownProps: {path: string[]}) => {
        const path = ownProps.path; // fixme doesn't work
        if(query.trim() == '') {
            dispatch(searchRequest(query, path));
            dispatch(searchResponse([], query, path));
            return;
        } // empty string => don't search
        dispatch(searchRequest(query, path));
        console.log("state.status", getState().status); // demonstration
        const baseUri = "//127.0.0.1:3000/search?";
        const terms = query.split(/\s+/);
        //const uri = baseUri + "limit=5&description=" + encodeURIComponent(`ilike.%${query}%`);
        const clauses = terms.map(t => '&description=ilike.' + encodeURIComponent(`%${t}%`));
        const uri = baseUri + "limit=5" + clauses.join('');
        fetch(uri)
            .then(resp => resp.json())
            .then(j => dispatch(searchResponse(j, query, path)) )
        // todo: handle errors
    }
});


export const Search = connect(mapStateToProps, mapDispatchToProps)(
    ({ result, onQueryChange, query}) => <SearchPresentation result={result} onQueryChange={onQueryChange} query={query} />
);


//  _______  __    _    __  __ ____  _     _____ ____
// | ____\ \/ /   / \  |  \/  |  _ \| |   | ____/ ___|
// |  _|  \  /   / _ \ | |\/| | |_) | |   |  _| \___ \
// | |___ /  \  / ___ \| |  | |  __/| |___| |___ ___) |
// |_____/_/\_\/_/   \_\_|  |_|_|   |_____|_____|____/
//

export const default_SearchExample =
    [{"source":"person","id":705,"title":"Аэлина Ахматова","description":"Аэлина Айнуровна Ахматова  Aelinaahmatova@gmail.com  "},
    {"source":"person","id":372,"title":"Алексей Шульга","description":"Алексей Андреевич Шульга    "},
    {"source":"course","id":302,"title":"Математический анализ-2","description":"Математический анализ-2 "},
    {"source":"person","id":840,"title":"Айдамир Иванов","description":"Айдамир Петрович Иванов  ivanov0745@icloud.com  "},
    {"source":"person","id":829,"title":"Анастасия Андреева","description":"Анастасия Михайловна Андреева  an_mi@mail.ru  "}]

export class SearchExample extends React.Component<any> {
    constructor(props: any){
        super(props);
        this.store = makeStore();
    }
    store: Store<{search: Map<number, SearchStateShape>}>;

    render() {
        return <Provider store={this.store}><div>
            { [1,2,3].map(i => <Search path={['search', i.toString()]} key={i}/>) }
        </div></Provider>
    }
}


//  ____ ___ ______   ______ _     _____
// | __ )_ _/ ___\ \ / / ___| |   | ____|
// |  _ \| | |    \ V / |   | |   |  _|
// | |_) | | |___  | || |___| |___| |___
// |____/___\____| |_| \____|_____|_____|
//

const Lens = ({
    get: (state: any, path: string[], initialState: any = undefined) => {
        let s = state;
        for(let p = 0; p < path.length; p++) {
            s = s[path[p]];
            if(typeof s == "undefined") return initialState;
        }
        return s;
    },

    set: function set(state: any, newLocalState: any, path: string[]): any {
        if(path.length == 0) return Object.assign({}, state, newLocalState);
        else {
            let [head, ...tail] = path;
            let subState = state[head];
            if(typeof subState == "undefined") subState = {};
            return Object.assign({}, state,
                {[head]: set(subState, newLocalState, tail)});
        }
    },

    localUpdate: function(state: any, localPatch: any, path: string[], initialState = {}) {
        let localState = Lens.get(state, path) || initialState;
        const patchState = Object.assign({}, localState, localPatch);
        return Lens.set(state, patchState, path);
    }
})
