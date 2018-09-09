import * as React from "react";
import 'react-dates/initialize'
import {DepartmentList, Person, PersonList, PersonSchool, School, SchoolList} from "../../generated/interfaces";
import 'react-dates/lib/css/_datepicker.css';
import {department_list, getRequest, person_fill, person_list} from "../../generated/api_connect";
import {Spinner} from "../common/Spinner";
import '../../../scss/person/person.scss'
import {ET} from "../common/EditableText";
import {ContactCard} from "../common/Cards/ContactCard";
import {Form} from "../common/Form";
import {Dropdown} from "../common/Dropdown";
import Select from 'react-select';
import '../../../scss/select_input_hack.scss'
import {DepartmentCard, DepartmentOption, DepartmentValue} from "../common/Cards/DepartmentCard";
import {Cut} from "../common/Cut";
import {SchoolCard} from "../common/Cards/SchoolCard";
import {CourseCard} from "../common/Cards/CourseCard";
import {ava} from "../common/utils";
import Async from "react-promise";
import {List} from "../common/List";
import {element} from "prop-types";
import {PersonExamList} from "./person_exam_list";
import {PersonCourseList} from "./person_course_list";
import {scalarMult} from "tweetnacl";

export interface PersonDashboardProps {
    person_id: number
}

export interface PersonDashboardState {
    person: Person
    departments: DepartmentList
}

export class PersonDashboard extends React.Component<PersonDashboardProps, PersonDashboardState> {
    constructor(props: any) {
        super(props);
        this.reload()
    }

    reload() {
        person_list({person_id: '' + this.props.person_id}).then((value: PersonList) => {
            if (value.length == 1) {
                person_fill(value.values[0]).then((valueP: Person) => {
                    department_list().then((valueD: DepartmentList) => {
                            this.setState({
                                departments: valueD,
                                person: valueP
                            })
                        }
                    )
                })
            } else {
                console.log(value);
                console.log("error")
            }
        });
    }

    render_contacts() {
        let contacts = [];
        for (let contact of this.state.person.contact_list.values) {
            contacts.push(<ContactCard contact={contact} del_btn={() => {
                getRequest('/admin/api/person/contact/del/' + contact.id, 'POST').then(() => {
                    this.reload()
                })
            }}/>)
        }
        return contacts;
    }

    render_contact_add() {
        return <div style={{display: 'inline-block'}}>
            <Dropdown label={'+'} component={
                <Form url={'/admin/api/person/contact/add/' + this.state.person.person_id}
                      entries={[
                          {
                              name: 'name',
                              text: 'Название, для почты - email'
                          },
                          {
                              name: 'url',
                              text: 'адрес'
                          }
                      ]}
                      onsubmit={() => {
                          this.reload()
                      }}
                />
            }/>

        </div>

    }

    change_department(value: any) {
        getRequest('/admin/api/person/department/change/'
            + this.state.person.person_id
            + '?department_id='
            + value.department_id, 'post').then((v: any) => {
                console.log(v);
                this.reload()
            }
        )
    }

    render_comments() {
        let comments = [];
        for (let person_comment of this.state.person.person_comment_list.values)
            comments.push(<div>{person_comment.comment_text}</div>)
        return <div className="person__additional__comments">
            <Cut label={"Комментарии"}
                 content={comments}/>
        </div>
    }

    render_exams() {
        let exams = <PersonExamList list={this.state.person.exam_list}/>;
        return <div className="person__additional__exams">
            <Cut label={"ЗачОты"}
                 content={exams}/>
        </div>
    }

    render_courses() {
        let courses = <PersonCourseList list={this.state.person.course_teachers_list}/>;
        return <div className="person__additional__courses">
            <Cut label={"Прочитанные курсы"}
                 content={courses}/>
        </div>
    }

    render_schools() {
        let schools = <List renderer={(school: School) => {
            return <SchoolCard school={school}
                               style={{
                                   display: 'flex',
                                   justifyContent: 'left'
                               }}
                               clickable={true}
            />
        }
        }
                            data={this.state.person.person_school_list.values.map((element: PersonSchool) => {
                                return element.school_id_fk
                            }).reverse()}
        />;
        return <div className="person__additional__schools">
            <Cut label={"Школы"} content={schools}/>
        </div>
    }

    render() {
        this.state ? console.log(this.state.person.department_id_fk.department_title) : null;
        return (this.state) ? <div className="person">
            <div className="person__title">
                <Async promise={ava(this.state.person)} then={val => {
                    return <img className="person__title__img" src={val}/>
                }}/>
                <div className="person__title__text">
                    <div className="person__title__text_fio">
                        {this.state.person.last_name ? <ET text={this.state.person.last_name} callback={() => {
                        }}/> : null}
                        {this.state.person.first_name ? <ET text={this.state.person.first_name} callback={() => {
                        }}/> : null}
                        {this.state.person.patronymic ? <ET text={this.state.person.patronymic} callback={() => {
                        }}/> : null}
                    </div>
                    {this.state.person.nick_name ? <ET text={this.state.person.nick_name} callback={() => {
                    }}/> : null}
                    <div className="person__title__text__department">
                        <span>Отделение:</span>
                        <Select onChange={(v: any) => {
                            this.change_department(v)
                        }}
                            // valueComponent={DepartmentValue}
                                optionComponent={DepartmentOption}
                                options={this.state.departments.values}
                                value={this.state.person.department_id_fk}
                                clearable={false}
                                className={'select_input_hack'}
                                wrapperStyle={{display: 'inline-block'}}
                                optionClassName={'entry'}
                        /></div>
                    <div className="person__title__text__contacts">
                        <span>Контакты:</span>
                        {this.render_contact_add()}{this.render_contacts()}</div>
                </div>
            </div>
            <div className="person__additional">
                {this.render_comments()}
                {this.render_exams()}
                {this.render_courses()}
                {this.render_schools()}
            </div>
        </div> : <Spinner/>
    }
}
