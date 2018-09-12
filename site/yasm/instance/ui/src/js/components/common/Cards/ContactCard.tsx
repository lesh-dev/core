import * as React from 'react'
import "../../../../scss/cards/contact_card/contact_card.scss"
import {CSSProperties} from "react";
import {Contact} from "../../../generated/interfaces";

export interface ContactCardProps {
    contact: Contact
    del_btn?: () => void
    style?: CSSProperties
}

export class ContactCard extends React.Component<ContactCardProps> {
    render_contact() {
        let name = this.props.contact.name;
        let link = this.props.contact.value;
        if (this.props.contact.name == 'email') {
            name = this.props.contact.value;
            link = 'mailto:' + this.props.contact.value;
        }
        return <a href={link}>{name}</a>

    }
    render_del_btn() {
        if (this.props.del_btn){
            return <div onClick={() => {this.props.del_btn()}}>
                ✗
            </div>
        }
        return null
    }
    render() {
        return <div className={"contact_card"} style={this.props.style}>
            {this.render_contact()}
            {this.render_del_btn()}
        </div>
    }
}