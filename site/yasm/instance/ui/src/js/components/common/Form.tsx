import * as React from 'react';
import {dict, getRequest} from "../../generated/api_connect";

export interface FormState {
    values: dict
}

export interface FormProps {
    url: string
    entries: { name: string, text: string }[]
    onsubmit?: () => void
}


export class Form extends React.Component<FormProps, FormState> {
    constructor(props: any) {
        super(props);
        let e = {} as dict;
        for (let entry of this.props.entries) {
            e[entry.name] = ('' as string)
        }
        this.state = {
            values: e
        }
    }

    change(event: any) {
        let tmp = this.state.values;
        tmp[event.target.name] = event.target.value;
        this.setState({values: tmp})
    }

    save() {
        let url = this.props.url;
        url += '?';
        for (let entry of this.props.entries) {
            url += entry.name + '=' + this.state.values[entry.name] + '&'
        }
        getRequest(url, 'POST');
        if (this.props.onsubmit) {
            this.props.onsubmit()
        }
    }

    render_form_content() {
        let e = [];
        for (let i = 0; i < this.props.entries.length; ++i) {
            e.push(<input placeholder={this.props.entries[i].text}
                          name={this.props.entries[i].name}
                          onChange={(e: any) => {
                              this.change(e)
                          }}
                          key={i}
            />)
        }
        return e
    }

    render() {
        return <div>
            <div>
                {this.render_form_content()}
            </div>
            <button onClick={() => {this.save()}}>сохранить</button>
        </div>
    }

}
