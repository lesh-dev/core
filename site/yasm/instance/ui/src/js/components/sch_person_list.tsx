import * as React from "react";
import {PersonSchool, PersonSchoolList} from "../generated/interfaces";
import Paper from '@material-ui/core/Paper';
import {IntegratedSorting, SortingState, FilteringState, IntegratedFiltering} from '@devexpress/dx-react-grid';
import {Grid, Table, TableFilterRow, TableHeaderRow} from '@devexpress/dx-react-grid-material-ui';

export interface SPListProps {
    spl: PersonSchoolList
}

export class SchPersonList extends React.Component<SPListProps, undefined> {
    render_dates(ps: PersonSchool) {
        return <div>TEST</div>
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
                dates: this.render_dates(this.props.spl.values[i])
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
                    {name: 'dates', title: "даты"}
                ]}>
                <FilteringState defaultFilters={[]}/>
                <IntegratedFiltering/>
                <SortingState
                    defaultSorting={[{columnName: 'last_name', direction: 'asc'}]}
                />
                <IntegratedSorting/>
                <Table/>
                <TableHeaderRow showSortingControls/>
                <TableFilterRow/>
            </Grid>
        </Paper>
    }
}