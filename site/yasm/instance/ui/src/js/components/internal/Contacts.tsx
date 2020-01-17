import * as React from 'react'
import {Contact, Person} from "../../generated/interfaces";
import {Edit} from "../common/Edit";
import {connect} from "react-redux";
import {commonActions, CommonState} from "../../redux-structure/common";
import {ReduxProps} from "../../redux-structure/store";

import {faPlusSquare} from "@fortawesome/free-regular-svg-icons/faPlusSquare";
import {faTrashAlt} from "@fortawesome/free-regular-svg-icons/faTrashAlt";
import {FontAwesomeIcon as FAIcon} from "@fortawesome/react-fontawesome";

import {ContactsPatchAction, ContactsPatch} from "../../api/internal/personal";

export interface ContactsProps {
    person: Person,
}

enum STATE {
    BASE,
    CHANGE,
}

export interface ContactsState {
    state: STATE,
    changes: ContactsPatch,
    currentAddition: {
        value: string,
        name: string,
    },
}

const initialState = {
    state: STATE.BASE,
    changes: new Map(),
    currentAddition: {
        value: '',
        name: '',
    },
}

@(connect((state: any) => state.common) as any)
export class Contacts extends React.Component<ContactsProps & CommonState & ReduxProps, ContactsState> {
    constructor(props: any) {
        super(props)
        this.state = initialState
    }

    private render_contact_prop(contact: Contact) {
        return contact.name
    }

    private render_contact_value(contact: Contact) {
        return contact.value
    }

    private prepare_changes(): Contact[] {
        return Array(...this.state.changes.entries()).filter(entry => (
            entry[1].action === ContactsPatchAction.ADD
        )).map(entry => ({
            value: entry[0],
            name: entry[1].name,
        } as Contact))
    }

    render() {
        switch (this.state.state) {
            case STATE.CHANGE:
            case STATE.BASE:
                return <>
                    <Edit
                        show={
                            this.props.person.person_id === this.props.login.profile.person_id
                        }
                        onClick={() => this.setState({
                            state: STATE.CHANGE,
                        })}
                        submit={
                            this.state.state === STATE.CHANGE
                        }
                        onSubmit={() => {
                            this.props.dispatch(commonActions.common.login.patchContacts(this.state.changes))
                            this.setState({
                                ...initialState,
                                changes: new Map(),
                            })
                        }}
                        style={{paddingRight: 30}}  // TODO (rebenkoy): to scss
                    >
                        {
                            this.props.person.contacts === undefined || this.props.person.contacts.length === 0
                                ? 'Что-то тут ничего нет'
                                : <>
                                    <table>
                                        <tbody>
                                            {
                                                this.props.person.contacts.concat(this.prepare_changes()).filter(contact => (
                                                    this.state.changes.get(contact.value) === undefined || this.state.changes.get(contact.value).action !== ContactsPatchAction.REMOVE
                                                )).map(contact => <tr>
                                                    <td>
                                                        {
                                                            this.render_contact_value(contact)
                                                        }
                                                    </td>
                                                    <td>
                                                        {
                                                            this.render_contact_prop(contact)
                                                        }
                                                    </td>
                                                    {
                                                        this.state.state === STATE.CHANGE
                                                        ?
                                                            <td>
                                                                <FAIcon icon={faTrashAlt} onClick={() => {
                                                                    const changes = this.state.changes
                                                                    changes.set(contact.value, {
                                                                        name: '',
                                                                        action: ContactsPatchAction.REMOVE,
                                                                    })
                                                                    this.setState({
                                                                        changes: changes,
                                                                    }
                                                                )}}/>
                                                            </td>
                                                        : null
                                                    }
                                                </tr>)
                                            }
                                            {
                                                this.state.state === STATE.CHANGE
                                                ?
                                                    <tr>
                                                        <td>
                                                            <input onChange={event => this.setState({
                                                                currentAddition: {
                                                                    ...this.state.currentAddition,
                                                                    value: event.target.value,
                                                                }
                                                            })}/>
                                                        </td>
                                                        <td>
                                                            <input onChange={event => this.setState({
                                                                currentAddition: {
                                                                    ...this.state.currentAddition,
                                                                    name: event.target.value,
                                                                }
                                                            })}/>
                                                        </td>
                                                        <td>
                                                            <FAIcon icon={faPlusSquare} onClick={() => {
                                                                const {value, name} = this.state.currentAddition
                                                                const changes = this.state.changes
                                                                changes.set(value, {
                                                                    name: name,
                                                                    action: ContactsPatchAction.ADD,
                                                                })
                                                                if (this.props.person.contacts.filter(c => c.value === value).length > 0) {
                                                                    changes.delete(value)
                                                                }
                                                                this.setState({
                                                                    changes: changes,
                                                                }
                                                            )}}/>
                                                        </td>
                                                    </tr>
                                                : null
                                            }
                                        </tbody>
                                    </table>
                                </>
                        }
                        </Edit>
                    </>
        }

    }
}