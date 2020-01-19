import * as React from 'react'

import {faSearch} from '@fortawesome/free-solid-svg-icons/faSearch'
import {FontAwesomeIcon as FAIcon} from '@fortawesome/react-fontawesome'

import '../../../scss/search-bar/search-bar.scss'
import {call} from "../../api/axios";
import {Link} from "react-router-dom";

interface Entry {
    search_url: string,
    data: any,
}

interface SearchBarState {
    focus: boolean,
    results: Entry[]
}

export class SearchBar extends React.Component<{}, SearchBarState>{
    rootRef = React.createRef<HTMLDivElement>()
    inputRef = React.createRef<HTMLInputElement>()
    timerId = null as NodeJS.Timeout
    constructor(props: any) {
        super(props)
        this.state = {
            focus: false,
            results: []
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
            call('/i/api/search', {query: value}).then(
                resp => resp.data
            ).then(data =>
                this.setState({
                    results: data,
                })
            )
        } else {
            this.setState({
                results: [],
            })
        }
    }

    private render_entry_value(data: {[idx: string]: string}) {
        let foundKey = null as string
        let foundIdx = -1
        for (const key of Object.keys(data)) {
            const value = (data[key] || '').toLowerCase()
            const idx = value.search(this.inputRef.current.value.toLowerCase())
            if (idx !== -1) {
                foundKey = key
                foundIdx = idx
            }
        }
        const start = Math.max(0, foundIdx - 5)
        const end = Math.min(data[foundKey].length, foundIdx + this.inputRef.current.value.length + 5)
        let value = data[foundKey].slice(start, end)
        if (start !== 0) {
            value = `...${value}`
        }
        if (end != data[foundKey].length) {
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
                    Object.entries(data).filter(([name, value]) => name !== foundKey).map(([name, value], i) => <div key={i}>
                        {
                            value
                        }
                    </div>)
                }
            </div>
        </div>
    }

    private render_entry(entry: Entry, i: number) {
        return <Link
            to={entry.search_url}
            className="search-bar__entry"
            key={i}
            onClick={() => this.setState({focus: false})}
        >
            {
                this.render_entry_value(entry.data)
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