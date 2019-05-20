import * as React from 'react';

declare var require: (filename: string) => any;
let {YMaps, Map, Placemark} = require("react-yandex-maps");
import {ET} from "../common/EditableText";

export interface LocationProps {
    location_text: string
    location_coords: string
    mapclick_callback: (e: any) => void
    text_edit_callback: (e: any) => void
}

export class Location extends React.Component<LocationProps> {
    onMapClick(e: any) {
        this.props.mapclick_callback(e)
    }

    onLocationChange(s: string) {
        this.props.text_edit_callback(s)
    }
    render() {
        return <div>
            <div className={"sch__location"}>
                <YMaps>
                    <Map state={{
                        center: this.props.location_coords ? this.props.location_coords.split(", ") : [55.748151, 37.617646],
                        zoom: 5
                    }} onClick={(e: any) => {
                        this.onMapClick(e)
                    }}>
                        {this.props.location_coords ? <Placemark
                            key={this.props.location_coords}
                            geometry={{coordinates: this.props.location_coords.split(", ")}}
                        /> : null}
                    </Map>
                </YMaps>
                <div className={"sch__location__text"}>
                    <ET text={this.props.location_text ? this.props.location_text : "Место не указано"}
                        callback={(s: string) => {
                            this.onLocationChange(s);
                        }}/>
                    <div>{this.props.location_coords}</div>
                </div>
            </div>
        </div>
    }
}