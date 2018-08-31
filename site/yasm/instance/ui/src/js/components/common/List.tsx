import * as React from "react";

export interface ListProps {
    renderer: any
    data: any[]
    prefix?: string
}


export class List extends React.Component<ListProps> {
    render_list() {
        let ans = [];
        for (let i = 0; i < this.props.data.length; ++i) {
            ans.push(this.props.renderer(this.props.data[i]));
        }
        return ans;
    }

    render() {
        return <div className="list">
            {this.render_list()}
        </div>
    }
}