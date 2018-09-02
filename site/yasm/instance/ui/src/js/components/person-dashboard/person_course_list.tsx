import * as React from "react";
import {CourseList, CourseTeachersList, PersonSchool, PersonSchoolList, School} from "../../generated/interfaces";
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
    TableRowDetail,
    Toolbar,
    TableColumnResizing
} from '@devexpress/dx-react-grid-material-ui';
import {PersonCard} from "../common/PersonCard";
import {SchoolCard} from "../common/SchoolCard";
import {CourseCard} from "../common/CourseCard";

export interface PersonCourseListProps {
    list: CourseTeachersList
}

const RowDetail = (row: any) => {
    return <div className={"details"}>
    </div>
};

interface PersonCourseListState {
    groupby_column: string
}

const groupingPanelMessages = {
    groupByColumn: 'Перетащите сюда колонку для группировки по ней',
};

const compareSchools = (a: any, b: any) => {
    return a.props.school.school_id < b.props.school.school_id ? -1 : 1;
};

export class PersonCourseList extends React.Component<PersonCourseListProps, PersonCourseListState> {
    constructor(props: any) {
        super(props);
        this.state = {
            groupby_column: 'department'
        }
    }

    gen_rows() {
        let list = [];
        for (let i = 0; i < this.props.list.length; ++i) {
            if (this.props.list.values[i].course_id_fk) {
                list.push({
                    title: <CourseCard course={this.props.list.values[i].course_id_fk} clickable={true}/>,
                    school: <SchoolCard school={this.props.list.values[i].course_id_fk.school_id_fk} clickable={true}/>,
                    area: this.props.list.values[i].course_id_fk.course_area,
                    cycle: this.props.list.values[i].course_id_fk.course_cycle
                });
            }
        }
        return list
    }

    render() {
        return <Paper>
            <Grid
                rows={this.gen_rows()}
                columns={[
                    {name: 'title', title: "Название"},
                    {name: 'cycle', title: "Цикл"},
                    {name: 'area', title: "Область"},
                    {name: 'school', title: "школа",},
                ]}>
                <DragDropProvider/>
                <FilteringState/>
                <IntegratedFiltering/>
                <SortingState
                    defaultSorting={[
                        {
                            columnName: 'school',
                            direction: 'desc'
                        }
                    ]}
                />
                <IntegratedSorting
                    columnExtensions={[
                        {
                            columnName: 'school',
                            compare: compareSchools
                        }
                    ]}
                />
                <GroupingState
                    grouping={[{
                        columnName: 'school'
                    }]}
                />
                <IntegratedGrouping
                    columnExtensions={[
                        {
                            columnName: 'school',
                            criteria: (school: any) => {
                                console.log(school);
                                return {
                                    key: school.props.school.school_id,
                                    value: school
                                }
                            }
                        }
                    ]}
                />
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
                    showGroupingControls={true}
                    showSortingControls={true}
                    messages={groupingPanelMessages}
                />
            </Grid>
        </Paper>
    }
}