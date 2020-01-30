import * as React from 'react'

import {faSearch} from '@fortawesome/free-solid-svg-icons/faSearch'
import {FontAwesomeIcon as FAIcon} from '@fortawesome/react-fontawesome'

import '../../../scss/search-bar/search-bar.scss'
import {call} from "../../api/axios";
import {Link} from "react-router-dom";

interface Entry<T> {
    search_url: string,
    data: T,
}

interface SearchBarState<T> {
    focus: boolean,
    results: Entry<T>[],
}

interface SearchBarProps<T> {
    tables?: string[]
    onClick?: (entry: T) => void
    display?: (entry: T) => React.ReactNode
}

export class SearchBar<T=any> extends React.Component<SearchBarProps<T>, SearchBarState<T>>{
    rootRef = React.createRef<HTMLDivElement>()
    inputRef = React.createRef<HTMLInputElement>()
    timerId = null as NodeJS.Timeout
    constructor(props: any) {
        super(props)
        this.state = {
            focus: false,
            results: [],
        }
        this.blur = this.blur.bind(this)
    }

    private blur(event: any) {
        if (this.rootRef && !this.rootRef.current.contains(event.target)) {
            this.setState({
                focus: false,
            })
        }
    }

    private searchCall(value: string) {
        if (value !== '') {
            const data = {
                query: value,
            } as any
            if (this.props.tables !== undefined) {
                data['tables'] = this.props.tables
            }
            call('/i/api/search', data).then(
                resp => resp.data
            ).then(data => {
                const new_query = String(data.query)
                if (new_query === this.inputRef.current.value) {
                    this.setState({
                        results: data.payload,
                    })
                }
            })
        } else {
            this.setState({
                results: [],
            })
        }
    }

    private render_entry_value(data: T) {
        if (this.props.display !== undefined) {
            return this.props.display(data)
        }
        const id_postfix = 'id'
        let foundKey = null as string
        let foundIdx = -1
        for (const key of Object.keys(data)) {
            if (!key.endsWith(id_postfix)) {
                const value = ((data as unknown as {[idx: string]: string})[key] || '').toLowerCase()
                const idx = value.indexOf(this.inputRef.current.value.toLowerCase())
                if (idx !== -1) {
                    foundKey = key
                    foundIdx = idx
                }
            }
        }
        if (foundKey === null) {
            return null
        }
        const start = Math.max(0, foundIdx - 5)
        const end = Math.min((data as unknown as {[idx: string]: string})[foundKey].length, foundIdx + this.inputRef.current.value.length + 5)
        let value = (data as unknown as {[idx: string]: string})[foundKey].slice(start, end)
        if (start !== 0) {
            value = `...${value}`
        }
        if (end != (data as unknown as {[idx: string]: string})[foundKey].length) {
            value = `${value}...`
        }
        return <div
            style={{display: 'flex'}}
        >
            <div
                style={{
                    marginRight: 32
                }}
            >
                {
                    value
                }
            </div>
            <div>
                {
                    Object.entries(data).filter(
                        ([name, value]) => name !== foundKey && !name.endsWith(id_postfix)
                    ).map(([name, value], i) => <div key={i}>
                        {
                            value
                        }
                    </div>)
                }
            </div>
        </div>
    }

    private render_entry(entry: Entry<T>, i: number) {
        const value = this.render_entry_value(entry.data)
        if (value === null) {
            return null
        }
        if (this.props.onClick !== undefined) {
            return <div
                className="search-bar__entry"
                key={i}
                onClick={() => {
                    this.setState({focus: false})
                    this.props.onClick(entry.data)
                }}
            >
                {
                    value
                }
            </div>
        }
        return <Link
            to={entry.search_url}
            className="search-bar__entry"
            key={i}
            onClick={() => this.setState({focus: false})}
        >
            {
                value
            }
        </Link>
    }

    componentDidMount(): void {
        document.addEventListener('mousedown', this.blur);
    }

    componentWillUnmount(): void {
        document.removeEventListener('mousedown', this.blur);
    }


    render() {
        return <div
            ref={this.rootRef}
            className="search-bar"
            onFocus={() => this.setState({
                focus: true,
            })}
        >
            <input
                ref={this.inputRef}
                className="search-bar__input"
                onChange={event => {
                    if (this.timerId !== null) {
                        clearTimeout(this.timerId)
                    }
                    this.timerId = setTimeout(() => this.searchCall(this.inputRef.current.value), 500)
                }}
            />
            <div
                className="search-bar__indicator"
            >
                <FAIcon
                    icon={faSearch}
                    size="2x"
                    onClick={() => this.inputRef.current.focus()}
                />
            </div>
            {
                this.state.focus
                ? <div
                    className="search-bar__results"
                >
                    {
                        this.state.results.map((entry, i) => this.render_entry(entry, i))
                    }
                </div>
                : null
            }
        </div>
    }
}