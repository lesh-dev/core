import * as React from "react";
import 'react-dates/initialize'
import {Person, PersonList, School, SchoolList} from "../../generated/interfaces";
import 'react-dates/lib/css/_datepicker.css';
import {getRequest, person_fill, person_list} from "../../generated/api_connect";
import {Spinner} from "../common/Spinner";
import '../../../scss/person/person.scss'
import {ET} from "../common/EditableText";
import {ContactCard} from "../common/ContactCard";
import {Form} from "../common/Form";
import {Dropdown} from "../common/Dropdown";


export interface PersonDashboardProps {
    person_id: number
}

export interface PersonDashboardState {
    person: Person
}

export class PersonDashboard extends React.Component<PersonDashboardProps, PersonDashboardState> {
    constructor(props: any) {
        super(props);
        this.reload()
    }

    reload() {
        person_list({person_id: '' + this.props.person_id}).then((value: PersonList) => {
            if (value.length == 1) {
                person_fill(value.values[0]).then((value: Person) => {
                    this.setState({person: value})
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
                getRequest('/admin/api/contact/del/' + contact.id, 'POST').then(() => {
                    this.reload()
                })
            }}/>)
        }
        return contacts;
    }

    render_contact_add() {
        return <div style={{display: 'inline-block'}}>
            <Dropdown label={'+'} component={
                <Form url={'/admin/api/contact/add/' + this.state.person.person_id}
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

    render() {
        return (this.state) ? <div className="person">
            <div className="person__title">
                <img className="person__title__img"
                     src="https://pp.userapi.com/c637326/v637326823/30fa0/By94QoUuQQs.jpg?ava=1"/>
                <div className="person__title__text">
                    <div style={{display: 'flex'}}>
                        {this.state.person.last_name ? <ET text={this.state.person.last_name} callback={() => {
                        }}/> : null}
                        {this.state.person.first_name ? <ET text={this.state.person.first_name} callback={() => {
                        }}/> : null}
                        {this.state.person.patronymic ? <ET text={this.state.person.patronymic} callback={() => {
                        }}/> : null}
                    </div>
                    {this.state.person.nick_name ? <ET text={this.state.person.nick_name} callback={() => {
                    }}/> : null}
                    <div>Отделение: <ET text={this.state.person.department_id_fk.department_title} callback={() => {
                    }}/></div>
                    <div>Контакты: {this.render_contact_add()}{this.render_contacts()}</div>
                </div>
            </div>
            <div className="person__additional">
            </div>
        </div> : <Spinner/>
    }
}
