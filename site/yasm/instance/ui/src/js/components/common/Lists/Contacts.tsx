import * as React from "react";
import {Person} from "../../../generated/interfaces";
import {ContactCard} from "../Cards/ContactCard";

function contacts(person: Person) {
    let contacts = [];
    for (let contact of person.contact) {
        contacts.push(<ContactCard contact={contact} del_btn={() => {
            // TODO: post to request ('/admin/api/person/contact/del/' + contact.id)
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