import * as React from "react";
import {ExamList, PersonSchool, PersonSchoolList, School} from "../../generated/interfaces";
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
import {PersonCard} from "../common/Cards/PersonCard";
import {SchoolCard} from "../common/Cards/SchoolCard";
import {CourseCard} from "../common/Cards/CourseCard";
import {SchoolToken} from "../common/Tokens/SchoolToken";

export interface PersonExamListProps {
    list: ExamList
}

const RowDetail = (row: any) => {
    return <div className={"details"}>
    </div>
};

interface PersonExamListState {
    groupby_column: string
}

const groupingPanelMessages = {
    groupByColumn: 'Перетащите сюда колонку для группировки по ней',
};

const compareSchools = (a: any, b: any) => {
    return a.props.school.school_id < b.props.school.school_id ? -1 : 1;
};

export class PersonExamList extends React.Component<PersonExamListProps, PersonExamListState> {
    constructor(props: any) {
        super(props);
        this.state = {
            groupby_column: 'department'
        }
    }

    gen_rows() {
        let list = [];
        for (let i = 0; i < this.props.list.length; ++i) {
            list.push({
                title: <CourseCard course={this.props.list.values[i].course_id_fk} clickable={true}/>,
                status: this.props.list.values[i].exam_status,
                school: <SchoolToken school={this.props.list.values[i].course_id_fk.school_id_fk} clickable={true}/>,
                area: this.props.list.values[i].course_id_fk.course_area
            });
        }
        return list
    }

    render() {
        return <Paper>
            <Grid
                rows={this.gen_rows()}
                columns={[
                    {name: 'title', title: "Название"},
                    {name: 'status', title: "Статус"},
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