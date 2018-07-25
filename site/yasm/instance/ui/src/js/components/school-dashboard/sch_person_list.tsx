import * as React from "react";
import {PersonSchool, PersonSchoolList} from "../../generated/interfaces";
import Paper from '@material-ui/core/Paper';
import {
    IntegratedSorting,
    SortingState,
    FilteringState,
    IntegratedFiltering,
    GroupingState, IntegratedGrouping, RowDetailState
} from '@devexpress/dx-react-grid';
import {
    DragDropProvider,
    Grid, GroupingPanel,
    Table,
    TableFilterRow,
    TableGroupRow,
    TableHeaderRow,
    TableRowDetail, Toolbar
} from '@devexpress/dx-react-grid-material-ui';
import {PersonCard} from "../common/PersonCard";

export interface SPListProps {
    spl: PersonSchoolList
    callback: (ps: number, value: any) => void
}

function render_status(row: any) {
    let status = "";
    if (row.teacher) {
        status += "препод"
    }
    if (row.cur_type == "assist") {
        if (status) {
            status += " / "
        }
        status += "помкур"
    }
    if (row.cur_type == "cur") {
        if (status) {
            status += " / "
        }
        status += "куратор"
    }
    if (row.student) {
        if (status) {
            status += " / "
        }
        status += "школьник";
    }
    return <div>Статус: {status}</div>
}

function render_nick(row: any) {
    if (row.nick) {
        return <div>{row.nick}</div>
    }
    return null
}

function render_grade(row: any) {
    if (row.student) {
        return <div>Класс: {row.grade}</div>
    }
    return null
}

function render_curator_group(row: any) {
    if (row.student) {
        return <div>Группа: {row.cur_group}</div>
    }
    return null
}

function render_exams(row: any) {
    if (row.student) {
        return <div>Неободимо зачётов: {row.courses_needed}</div>
    }
    return null
}

function render_dates(row: any) {
    return <div className={"inline_dates"}>
        <div>На школе:</div>
        <div style={{width: "1em"}}></div>
        <div>
            <div>с
                {row.date_start}
            </div>
            <div>по
                {row.date_end}
            </div>
        </div>
    </div>
}

function render_changes(row: any) {
    return <div className={"inline_mod"}>
            <div>{row.changed_by}</div>
            <div>{row.changed_at}</div>
        </div>
}

const RowDetail = (row: any) => {
    return <div className={"details"}>
        <PersonCard person={row.row} clickable={true}/>
        {render_nick(row.row)}
        {render_status(row.row)}
        {render_grade(row.row)}
        {render_curator_group(row.row)}
        {render_dates(row.row)}
        {render_exams(row.row)}
        {render_changes(row.row)}
    </div>
};

interface SPListState {
    groupby_column: string
}

const groupingPanelMessages = {
    groupByColumn: 'Перетащите сюда колонку для группировки по ней',
};

export class SchPersonList extends React.Component<SPListProps, SPListState> {
    constructor(props: any) {
        super(props);
        this.state = {
            groupby_column: 'department'
        }
    }

    render_dates(ps: PersonSchool, i: number) {
        return <div></div>
    }

    gen_rows() {
        let list = [];
        for (let i = 0; i < this.props.spl.length; ++i) {
            let department: string;
            if (this.props.spl.values[i].member_department_id_fk.department_title) {
                department = this.props.spl.values[i].member_department_id_fk.department_title
            } else {
                department = this.props.spl.values[i].member_person_id_fk.department_id_fk.department_title
            }

            list.push({
                last_name: this.props.spl.values[i].member_person_id_fk.last_name,
                first_name: this.props.spl.values[i].member_person_id_fk.first_name,
                patronymic: this.props.spl.values[i].member_person_id_fk.patronymic,
                department: department,
                dates: this.render_dates(this.props.spl.values[i], i),
                grade: this.props.spl.values[i].member_person_id_fk.current_class,
                teacher: this.props.spl.values[i].is_teacher,
                student: this.props.spl.values[i].is_student,
                cur_type: this.props.spl.values[i].curatorship,
                cur_group: this.props.spl.values[i].curator_group,
                courses_needed: this.props.spl.values[i].courses_needed,
                changed_by: this.props.spl.values[i].person_school_changedby,
                changed_at: (this.props.spl.values[i].person_school_modified) ? this.props.spl.values[i].person_school_modified : this.props.spl.values[i].person_school_created,
                comment: this.props.spl.values[i].person_school_comment,
                date_start: this.props.spl.values[i].frm,
                date_end: this.props.spl.values[i].tll,
                nick: this.props.spl.values[i].member_person_id_fk.nick_name,
                person_id: this.props.spl.values[i].member_person_id
            });
        }
        return list
    }

    render() {
        return <Paper>
            <Grid
                rows={this.gen_rows()}
                columns={[
                    {name: 'last_name', title: "Фамилия"},
                    {name: 'first_name', title: "Имя"},
                    {name: 'patronymic', title: "Отчество"},
                    {name: 'department', title: "Отделение"},
                    {name: 'cycles', title: "циклы"}
                ]}>
                <DragDropProvider/>
                <FilteringState
                    columnExtensions={[
                        {columnName: 'cycles', filteringEnabled: false},
                    ]}
                />
                <IntegratedFiltering/>
                <SortingState
                    defaultSorting={[{columnName: 'last_name', direction: 'asc'}]}
                    columnExtensions={[
                        {columnName: 'cycles', sortingEnabled: false},
                    ]}
                />
                <IntegratedSorting/>
                <GroupingState
                    columnExtensions={[
                        {columnName: 'cycles', groupingEnabled: false}
                    ]}
                />
                <IntegratedGrouping/>
                <RowDetailState
                    defaultExpandedRowIds={[]}
                />
                <Table/>
                <TableHeaderRow showSortingControls/>
                <TableFilterRow/>
                <TableGroupRow/>
                <TableRowDetail
                    contentComponent={RowDetail}
                />
                <Toolbar/>
                <GroupingPanel
                    showGroupingControls
                    messages={groupingPanelMessages}
                />
            </Grid>
        </Paper>
    }
}