import * as React from "react";
import {getRequest} from "../../../generated/api_connect";
import {Person} from "../../../generated/interfaces";
import {ContactCard} from "../Cards/ContactCard";

function contacts(person: Person) {
    let contacts = [];
    for (let contact of person.contact_list.values) {
        contacts.push(<ContactCard contact={contact} del_btn={() => {
            getRequest('/admin/api/person/contact/del/' + contact.id, 'POST').then(() => {
                this.reload()
            })
        }}/>)
    }
    return contacts;
}

export interface ContactsProps {
    person: Person
}

export class Contacts extends React.Component<ContactsProps> {
    render() {
        return <div className={"contacts"}>
            {contacts(this.props.person)}
        </div>
    }
}