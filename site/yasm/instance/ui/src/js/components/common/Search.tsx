import * as React from "react"
import {connect, Provider, Store} from "react-redux"
import {applyMiddleware, createStore} from "redux"
import thunkMiddleware from 'redux-thunk'
import { createLogger } from 'redux-logger'
import { composeWithDevTools } from 'redux-devtools-extension'

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


class SnippetHelper {
    // входит ли index-ный символ строки content вкакую-нибудь подстроку, равную term?
    check(content: string, term: string, index: number): boolean {
        let startIndex = 0;
        do {
            let i = content.toLowerCase().indexOf(term.toLowerCase(), startIndex);
            if(i == -1) return false;
            if(i <= index && index < i + term.length && i > -1) {
                return true;
            }
            startIndex++;
        } while(startIndex <= index);
        return false;
    }

    // для строки-контента и массива строк-запросов считает, какие буквы надо подсветить
    toHighlights(content: string, search: string[]) {
        // в цикле проходим по строке, проверяем, входит ли символ в один из запросов
        // Тупо, без Кнута-Морриса-Пратта и прочих.
        return content.split('').map((_l,i) => {
            for(let j = 0; j < search.length; j++) {
                if (this.check(content, search[j], i)) {
                    return {index: i, letter: content[i], highlight: true};
                }
            }
            return {index: i, letter: content[i], highlight: false};
        })
    }

    groupHighlights(hs: {index:number, letter:string, highlight:boolean} []) {
        let groups = [];
        let currentGroup = [];
        let currentHighlight = false; // does not matter
        for(let i = 0; i < hs.length; i++) {
            if(hs[i].highlight == currentHighlight) {
                currentGroup.push(hs[i])
            }
            else {
                groups.push(currentGroup);
                currentGroup = [];
                currentGroup.push(hs[i]);
                currentHighlight = hs[i].highlight;
            }
        }
        groups.push(currentGroup);
        return groups.filter(x => x.length > 0)
            .map(group => ({ highlight: group[0].highlight, str: group.map(h=>h.letter).join('') }));
    }

    groups(content: string, search: string[]) {
        return this.groupHighlights(this.toHighlights(content, search))
    }

    toHighlightedHtml = (group: {str: string, highlight: boolean}, key: string) => {
        if(group.highlight) return <span key={key} style={{backgroundColor: 'yellow'}}>{group.str}</span>;
        else return group.str;
    }

}

const snippetHelper = new SnippetHelper;

const HighlightTitle = (props: any) => {
    let search = props.query.split(/\s+/);
    let groups = snippetHelper.groups(props.title, search);
    return groups.map((g, i) => {
        if(g.highlight) return <span style={{backgroundColor: 'yellow'}} key={i}>{g.str}</span>;
        else return g.str;
    });
}

export class Snippet extends React.Component<{ query: string, stopwords: string, content: string }> {
    render() {
        let stops = this.props.stopwords.split(/\s+/)
            .map(s => s.toLowerCase());
        let terms = this.props.query.split(/\s+/)
            .map(s => s.toLowerCase());
        let words = this.props.content.split(/\s+/);
        let newWords = words.filter(w => stops.indexOf(w.toLowerCase()) == -1); // don't repeat title
        let groups/* : {...}[][] */ = newWords.map(w => snippetHelper.groups(w, terms))
            .filter(group => group.some(item => item.highlight));
        const space = { str: ' ', highlight: false };
        let items = groups.reduce((g1, g2) => g1.concat([space], g2), []);
        let html = items.map((item, i) => snippetHelper.toHighlightedHtml(item, i.toString()));
        return <span style={{fontSize: '0.75em'}}>{html}</span>
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
