import * as React from 'react'
import * as _ from 'lodash'
import {v4 as uuid} from 'uuid';
import {faArrowAltCircleDown, faArrowAltCircleUp, faDotCircle} from "@fortawesome/free-regular-svg-icons"
import {faTimes} from "@fortawesome/free-solid-svg-icons"
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome"

const {Draggable, Droppable} = require('react-drag-and-drop')

interface ColumnProps {
    value: ((row: any) => any) | string
    title?: string

    sortKey?: (row: any) => any
    sortable?: boolean

    groupExtract?: (row: any) => any
    groupKey?: (group: any) => any
    groupValue?: (group: any) => any
    groupSortable?: boolean
    groupSortKey?: (group: any) => any
    groupable?: boolean
}

interface HeaderProps {
    columns: ColumnProps[]
}

interface ColumnPropsDirect {
    value: (row: any) => any
    title: string

    sortKey?: (row: any) => any
    sortable: boolean

    groupExtract?: (row: any) => any
    groupKey?: (group: any) => any
    groupValue?: (group: any) => any
    groupSortable: boolean
    groupSortKey?: (group: any) => any
    groupable: boolean

    id: number
}

interface HeaderPropsDirect {
    columns: ColumnPropsDirect[]
    hasGroupable: boolean
}

function patchHeader(header: HeaderProps): HeaderPropsDirect {
    let head = {columns: []} as HeaderPropsDirect
    let id = 0
    for (const column of header.columns) {
        const col = {} as ColumnPropsDirect
        if (column.title === null || column.title === undefined) {
            if (!((typeof column.value) === "string")) {
                throw {
                    descr: 'Check your table header declaration: in header, got column with no title and not string value',
                    header: header,
                    column: column,
                }
            } else {
                col.title = column.value as string
                col.value = (row: any) => row[column.value as string]
            }
        } else {
            col.title = column.title
            if ((typeof column.value) === "string") {
                col.value = (row: any) => row[column.value as string]
            }
        }
        if (column.groupable) {
            head.hasGroupable = true
            col.groupable = true
            col.groupExtract = column.groupExtract || col.value
            col.groupKey = column.groupKey || (grp => grp)
            col.groupValue = column.groupValue || (grp => grp)
            col.groupSortable = column.groupSortable || true
            if (col.groupSortable) {
                col.groupSortKey = column.groupSortKey || column.sortKey || (grp => grp)
            }
        } else {
            col.groupable = false
        }
        if (column.sortable) {
            col.sortable = true
            if (!column.sortKey) {
                col.sortKey = col.value
            } else {
                col.sortKey = column.sortKey
            }
        } else {
            col.sortable = false
        }
        col.id = id
        id += 1
        head.columns.push(col)
    }
    return head
}

interface TableProps {
    header: HeaderProps
    content: any[]
}

interface TablePropsDirect {
    header: HeaderPropsDirect
    content: any[]
}

enum SortDirection {
    asc,
    desc,
    none,
}

function nextDirection(direction: SortDirection) {
    switch (direction) {
        case SortDirection.asc:
            return SortDirection.desc
        case SortDirection.desc:
            return SortDirection.none
        case SortDirection.none:
            return SortDirection.asc
    }
}

function directionIcon(direction: SortDirection) {
    switch (direction) {
        case SortDirection.asc:
            return faArrowAltCircleDown
        case SortDirection.desc:
            return faArrowAltCircleUp
        case SortDirection.none:
            return faDotCircle
    }
}

interface GroupStateDirect {
    groupBy: number
    sortedDirection?: SortDirection
}

interface TableStateDirect {
    grouping: GroupStateDirect[]
    sortedBy?: number
    sortedDirection?: SortDirection
    uuid: string
}

export class TableDirect extends React.Component<TablePropsDirect, TableStateDirect> {
    constructor(props: TablePropsDirect) {
        super(props)
        this.state = {
            uuid: uuid(),
            grouping: [],
        }
    }

    sortedClickHandler(id: number) {
        if (this.props.header.columns[id].sortable) {
            if (this.state.sortedBy === id) {
                this.setState({sortedDirection: nextDirection(this.state.sortedDirection)})
            } else {
                this.setState({
                    sortedBy: id,
                    sortedDirection: SortDirection.asc,
                })
            }
        }
    }

    buildDataRow(content: any, idx: number, columns: ColumnPropsDirect[]) {
        const cols = []
        let newGroup = false
        for (let i = 0; i < this.state.grouping.length; ++i) {
            const grouping = this.state.grouping[i]
            let col = this.props.header.columns[grouping.groupBy]
            if (!newGroup && idx > 0) {
                if (col.groupKey(col.groupExtract(content[idx].row)) !== col.groupKey(col.groupExtract(content[idx - 1].row))) {
                    newGroup = true
                }
            } else {
                newGroup = true
            }
            if (newGroup) {
                cols.push(
                    <td key={col.id} rowSpan={content[idx].grpAnnotation[i]}>
                        {col.groupValue(col.groupExtract(content[idx].row))}
                    </td>
                )
            }
        }
        columns.map(col => cols.push(
            <td>
                {col.value(content[idx].row)}
            </td>
        ))
        return cols
    }

    buildDataTable(content: any[], columns: ColumnPropsDirect[]) {
        const rows = []
        for (let i = 0; i < content.length; ++i) {
            rows.push(
                <tr key={i}>
                    {this.buildDataRow(content, i, columns)}
                </tr>
            )
        }
        return rows
    }

    addGrouping(data: any) {
        const grouping = this.state.grouping
        const id = Number(data[this.state.uuid])
        if (this.props.header.columns[id].groupable) {
            grouping.push({
                groupBy: id,
                sortedDirection: SortDirection.none,
            })
            this.setState({
                grouping: grouping
            })
        }
    }

    removeGrouping(id: number) {
        const grouping = this.state.grouping.filter(col => col.groupBy !== id)
        this.setState({
            grouping: grouping
        })
    }

    groupSortHandler(idx: number) {
        const grouping = this.state.grouping
        grouping[idx].sortedDirection = nextDirection(grouping[idx].sortedDirection)
        this.setState({grouping: grouping})
    }

    group(content: any, idx: number = 0) {
        if (idx >= this.state.grouping.length) {
            if (this.state.sortedBy) {
                switch (this.state.sortedDirection) {
                    case SortDirection.none:
                        console.log("NONE")
                        break
                    case SortDirection.asc:
                        console.log("ASC")
                        content = _.orderBy(content, row => (
                            this.props.header.columns[this.state.sortedBy].sortKey(row)
                        ), 'asc')
                        break
                    case SortDirection.desc:
                        content = _.orderBy(content, row => (
                            this.props.header.columns[this.state.sortedBy].sortKey(row)
                        ), 'desc')
                        break
                }
            }
            return content.map((row: any) => ({row: row, grpAnnotation: {}}))
        }
        const grouping = this.state.grouping[idx]
        const c = this.props.header.columns[grouping.groupBy]
        content = Object.values(_.groupBy(content, (row: any) => c.groupKey(c.groupExtract(row))))
        switch (this.state.grouping[idx].sortedDirection) {
            case SortDirection.none:
                break
            case SortDirection.desc:
                content = _.orderBy(content, (row: any) => c.groupSortKey(c.groupExtract(row[0])), 'desc')
                break
            case SortDirection.asc:
                content = _.orderBy(content, (row: any) => c.groupSortKey(c.groupExtract(row[0])), 'asc')
                break
        }
        for (let i = 0; i < content.length; ++i) {
            content[i] = this.group(content[i], idx + 1)
            content[i][0].grpAnnotation[idx] = content[i].length
        }
        return _.flatten(content)
    }

    render() {
        let groupColumns = [] as ColumnPropsDirect[]
        for (let i = 0; i < this.state.grouping.length; ++i) {
            groupColumns.push({} as ColumnPropsDirect)
        }
        let columns = [] as ColumnPropsDirect[]
        for (const column of this.props.header.columns) {
            const place = this.state.grouping.findIndex(d => d.groupBy === column.id)
            if (place !== -1) {
                groupColumns[place] = column
            } else {
                columns.push(column)
            }
        }
        return (
            <table>
                <thead>
                {
                    this.props.header.hasGroupable
                    ? (
                        <tr>
                            <th colSpan={this.props.header.columns.length} onDragOver={event => event.preventDefault()}>
                                <Droppable
                                    types={[this.state.uuid]}
                                    onDrop={(data: any) => this.addGrouping(data)}
                                >
                                    Группировка:
                                    {groupColumns.map(column => (
                                        <span>
                                            {column.title}
                                            <span onClick={() => this.removeGrouping(column.id)}>
                                                <FontAwesomeIcon icon={faTimes}/>
                                            </span>
                                        </span>
                                    ))}
                                </Droppable>
                            </th>
                        </tr>
                    )
                    : null
                }
                <tr>
                    {groupColumns.map((column, index) => (
                        <th onClick={() => this.groupSortHandler(index)}>
                            {column.title}{column.groupSortable
                            ? <FontAwesomeIcon icon={directionIcon(this.state.grouping[index].sortedDirection)}/>
                            : null}
                        </th>
                    ))}
                    {columns.map(col => (
                        <th onClick={() => this.sortedClickHandler(col.id)} draggable={col.groupable}>
                            <Draggable type={this.state.uuid} data={col.id}>
                                {col.title}{col.sortable ? <FontAwesomeIcon icon={
                                this.state.sortedBy === col.id
                                    ? directionIcon(this.state.sortedDirection)
                                    : faDotCircle
                            }/> : null}
                            </Draggable>
                        </th>
                    ))}
                </tr>
                </thead>
                <tbody>
                {this.buildDataTable(this.group(this.props.content), columns)}
                </tbody>
            </table>
        )
    }
}

export class Table extends React.Component
    <TableProps> {
    render() {
        return <TableDirect
            header={patchHeader(this.props.header)}
            content={this.props.content}
        />
    }
}
