import * as React from "react";

export interface ImgGalleryProps {
    width: number
    height: number
    imgs: string[]
}

export class ImgGallery extends React.Component<ImgGalleryProps> {
    public render() {
        return <div style={{...this.props, overflow: 'hidden'}}>
            {
                this.props.imgs.map((img, i) => <img src={img} key={i} height={this.props.height}/>)
            }
        </div>
    }
}