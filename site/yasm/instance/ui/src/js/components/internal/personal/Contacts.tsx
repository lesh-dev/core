import * as React from 'react'
import {Contact, Person} from "../../../generated/frontend/interfaces/yasm/database";
import {Edit} from "../../common/Edit";
import {connect} from "react-redux";
import {commonActions, CommonState} from "../../../redux-structure/common";
import {ReduxProps} from "../../../redux-structure/store";

import {faPlusSquare} from "@fortawesome/free-regular-svg-icons/faPlusSquare";
import {faTrashAlt} from "@fortawesome/free-regular-svg-icons/faTrashAlt";
import {FontAwesomeIcon as FAIcon} from "@fortawesome/react-fontawesome";

import {ContactsPatch, ContactsPatchActions} from "../../../generated/frontend/interfaces/yasm/internal/person";

export interface ContactsProps {
    person: Person,
}

enum STATE {
    BASE,
    CHANGE,
}

type Patch = Map<string, {
    name: string,
    action: ContactsPatchActions,
}>

export interface ContactsState {
    state: STATE,
    changes: Patch,
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
            entry[1].action === ContactsPatchActions.add
        )).map(entry => ({
            value: entry[0],
            name: entry[1].name,
        } as Contact))
    }


    private prepare_submit(patch: Patch): ContactsPatch {
        const ret = {} as ContactsPatch.PatchEntry
        for (const [value, state] of patch.entries()) {
            ret[value] = state
        }
        return {'patch': ret}
    }

    render() {
        switch (this.state.state) {
            case STATE.CHANGE:
            case STATE.BASE:
                return <>
                    <Edit
                        edit={
                            this.props.person.id === this.props.login.profile.id
                        }
                        onClick={() => this.setState({
                            state: STATE.CHANGE,
                        })}
                        submit={
                            this.state.state === STATE.CHANGE
                        }
                        onSubmit={() => {
                            console.log(this.state.changes)
                            this.props.dispatch(commonActions.common.login.patchContacts(this.prepare_submit(this.state.changes)))
                            this.setState({
                                ...initialState,
                                changes: new Map(),
                            })
                        }}
                        style={{paddingRight: 30}}  // TODO (rebenkoy): to scss
                    >
                    {
                        this.props.person.contacts === undefined || this.props.person.contacts.length === 0
                            ? 'пока тут пусто'
                            : <>
                                <table style={{width: 400}}>
                                    <tbody>
                                        {
                                            this.props.person.contacts.concat(this.prepare_changes()).filter(contact => (
                                                this.state.changes.get(contact.value) === undefined || this.state.changes.get(contact.value).action !== ContactsPatchActions.remove
                                            )).map((contact, i) => <tr
                                                key={i}
                                            >
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
                                                                    action: ContactsPatchActions.remove,
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
                                                                action: ContactsPatchActions.add,
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