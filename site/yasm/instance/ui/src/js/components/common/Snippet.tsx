import * as React from "react";

export class SnippetHelper {
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
        if(group.highlight)
            return <span key={key} className={"snippet__description_highlight"}>{group.str}</span>;
        else return group.str;
    }

}

export const snippetHelper = new SnippetHelper;

export const HighlightTitle = (props: {query: string, title: string}) => {
    let search = props.query.split(/\s+/);
    let groups = snippetHelper.groups(props.title, search);
    return groups.map((g, i) => {
        if(g.highlight) return <span className={"snippet__title_highlight"} key={i}>{g.str}</span>;
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
        const space = { str: ' ', highlight: false, index: -1 };
        let items = groups.reduce((g1, g2) => g1.concat([space], g2), []);
        let html = items.map((item, i) => snippetHelper.toHighlightedHtml(item, i.toString()));
        return <span className={"snippet__description"}>{html}</span>
    }
}




//  _______  __    _    __  __ ____  _     _____ ____
// | ____\ \/ /   / \  |  \/  |  _ \| |   | ____/ ___|
// |  _|  \  /   / _ \ | |\/| | |_) | |   |  _| \___ \
// | |___ /  \  / ___ \| |  | |  __/| |___| |___ ___) |
// |_____/_/\_\/_/   \_\_|  |_|_|   |_____|_____|____/
//

export class TestHighlight extends React.Component
    <{}, {query: string, title: string, description: string}> {
    constructor(props: any) {
        super(props);
        this.state = {
            query: 'й а',
            title: 'Анна Михайловна',
            description: 'Анна Михайловна Проверка proverka@gmail.com слово без этих букв'
        }
        this.handleQuery = this.handleQuery.bind(this);
        this.handleTitle = this.handleTitle.bind(this);
        this.handleDescription = this.handleDescription.bind(this);
    }
    handleQuery = (e:any) => this.setState({ query: e.target.value });
    handleTitle = (e:any) => this.setState({ title: e.target.value });
    handleDescription = (e:any) => this.setState({ description: e.target.value });

    getKeywords = () => this.state.query.split(/\s+/);

    render() {
        return (<div>
            <p>Ключевые слова для поиска:
                <input type='text' value={this.state.query}
                   onChange={this.handleQuery}
                   placeholder='query'/></p>
            <p>Загловок результата поиска:
                <input type='text' value={this.state.title}
                   onChange={this.handleTitle}
                   placeholder='title'/></p>

            <p>В заголовке должны подсвечиваться все вхождения ключевых слов:</p>
            <span children={ HighlightTitle(this.state) }/>

            <p>Подробное описание результата поиска:</p>
            <textarea value={this.state.description}
                      onChange={this.handleDescription}/>
            <p>В сниппете должны быть перечислены все слова описания,
               в которых найдены ключевые слова, кроме слов из заголовка,
               и должны подсвечиваться все вхождения ключевых слов:</p>
            <Snippet query={this.state.query} stopwords={this.state.title} content={this.state.description}/>

        </div>);
    }
}