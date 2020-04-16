import * as React from 'react'

import {faSearch} from '@fortawesome/free-solid-svg-icons/faSearch'
import {FontAwesomeIcon as FAIcon} from '@fortawesome/react-fontawesome'

import '../../../scss/search-bar/search-bar.scss'
import {Link} from "react-router-dom";
import { APIBuiltin } from "../../generated/frontend/services/builtin";
import { SearchResponse } from "../../generated/frontend/interfaces/builtin";
import {PersonCard} from "./Cards/PersonCard";
import {Department, Person, School, Course} from "../../generated/frontend/interfaces/yasm/database";
import {DepartmentCard} from "./Cards/DepartmentCard";
import {CourseCard} from "./Cards/CourseCard";
import {SchoolCard} from "./Cards/SchoolCard";


interface SearchBarState {
    focus: boolean,
    results: SearchResponse,
}

interface Dispatcher<T> {
    person?: (entry: Person, key?: number) => T
    department?: (entry: Department, key?: number) => T
    school?: (entry: School, key?: number) => T
    course?: (entry: Course, key?: number) => T
}

interface SearchBarProps<T> {
    tables?: string[]
    onClick?: Dispatcher<void>
    display?: Dispatcher<React.ReactNode>
}

export class SearchBar<T=any> extends React.Component<SearchBarProps<T>, SearchBarState>{
    static defaultProps = {
        display: {},
        onClick: {},
    }
    rootRef = React.createRef<HTMLDivElement>()
    inputRef = React.createRef<HTMLInputElement>()
    timerId = null as NodeJS.Timeout
    constructor(props: any) {
        super(props)
        this.state = {
            focus: false,
            results: {},
        }
        this.blur = this.blur.bind(this)
        this.render_person = this.render_person.bind(this)
        this.render_department = this.render_department.bind(this)
        this.render_school = this.render_school.bind(this)
        this.render_course = this.render_course.bind(this)
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
            APIBuiltin.Search(data).then(
                resp => resp.data
            ).then(data => {
                const new_query = String(data.query)
                if (new_query === this.inputRef.current.value) {
                    this.setState({
                        results: data,
                    })
                }
            })
        } else {
            this.setState({
                results: {},
            })
        }
    }

    private render_person(entry: Person, key: number) {
        const value = <PersonCard person={entry} key={key}/>
        if (this.props.onClick.person !== undefined) {
            return <div
                className="search-bar__entry"
                key={key}
                onClick={() => {
                    this.setState({focus: false})
                    this.props.onClick.person(entry)
                }}
            >
                {
                    value
                }
            </div>
        }
        return <Link
            to={`/i/person/${entry.id}`}
            className="search-bar__entry"
            key={key}
            onClick={() => this.setState({focus: false})}
        >
            {
                value
            }
        </Link>
    }

    private render_course(entry: Course, key: number) {
        const value = <CourseCard course={entry} key={key}/>
        if (this.props.onClick.person !== undefined) {
            return <div
                className="search-bar__entry"
                key={key}
                onClick={() => {
                    this.setState({focus: false})
                    this.props.onClick.course(entry)
                }}
            >
                {
                    value
                }
            </div>
        }
        return <Link
            to={`/i/course/${entry.id}`}
            className="search-bar__entry"
            key={key}
            onClick={() => this.setState({focus: false})}
        >
            {
                value
            }
        </Link>
    }

    private render_school(entry: School, key: number) {
        const value = <SchoolCard school={entry} key={key}/>
        if (this.props.onClick.person !== undefined) {
            return <div
                className="search-bar__entry"
                key={key}
                onClick={() => {
                    this.setState({focus: false})
                    this.props.onClick.person(entry)
                }}
            >
                {
                    value
                }
            </div>
        }
        return <Link
            to={`/i/school/${entry.id}`}
            className="search-bar__entry"
            key={key}
            onClick={() => this.setState({focus: false})}
        >
            {
                value
            }
        </Link>
    }

    private render_department(entry: Department, key: number) {
        const value = <DepartmentCard department={entry} key={key}/>
        if (this.props.onClick.department !== undefined) {
            return <div
                className="search-bar__entry"
                key={key}
                onClick={() => {
                    this.setState({focus: false})
                    this.props.onClick.department(entry)
                }}
            >
                {
                    value
                }
            </div>
        }
        return <Link
            to={`/i/department/${entry.id}`}
            className="search-bar__entry"
            key={key}
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
        const person_renderer = this.props.display.person || this.render_person
        const department_renderer = this.props.display.department || this.render_department
        const course_renderer = this.props.display.course || this.render_course
        const school_renderer = this.props.display.school || this.render_school
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
                        this.state.results.person
                            ? this.state.results.person.map(person_renderer)
                            : null
                    }
                    {
                        this.state.results.department
                            ? this.state.results.department.map(department_renderer)
                            : null
                    }
                    {
                        this.state.results.course
                            ? this.state.results.course.map(course_renderer)
                            : null
                    }
                    {
                        this.state.results.school
                            ? this.state.results.school.map(school_renderer)
                            : null
                    }
                </div>
                : null
            }
        </div>
    }
}