import * as React from "react";
import {Person} from "../../../generated/interfaces";
import {connect} from "react-redux";
import {commonActions, CommonState} from "../../../redux-structure/common";
import {ReduxProps} from "../../../redux-structure/store";
import {Edit} from "../../common/Edit";
import {Modal} from "../../common/Modal";
import {Button} from "../../common/Button";
import Cropper from 'react-easy-crop'
import {Area, Point} from "react-easy-crop/types";
import {getCroppedImg} from "../../../util/ImageCrop";

// @ts-ignore
import Incognito from '../../../../assets/incognito.svg'

export interface BigAvaProps {
    person: Person,
}

enum STATE {
    BASE,
    CHANGE,
    PREVIEW,
    LOADING,
}

export interface BigAvaState {
    state: STATE,
    image: string,
    newImage: string,
    crop: Point,
    zoom: number,
}

const initialState = {
    state: STATE.BASE,
    image: '',
    newImage: '',
    crop: {
        x: 0,
        y: 0,
    },
    zoom: 1,
}

@(connect((state: any) => state.common) as any)
export class BigAva extends React.Component<BigAvaProps & CommonState & ReduxProps, BigAvaState>{
    constructor(props: any) {
        super(props)

        this.state = initialState
    }
    inputRef = React.createRef<HTMLInputElement>()

    private imageChange(event: React.ChangeEvent<HTMLInputElement>): null {
        if (event.target.files.length == 0) {
            return null
        } else if (event.target.files.length > 1) {
            console.warn('multiple files TODO')
            return null
        }
        const file = event.target.files[0]
        const reader = new FileReader()
        reader.onloadend = e => {
            this.setState({
                state: STATE.CHANGE,
                image: reader.result as string,
            })
        }
        reader.readAsDataURL(file)

    }

    private submitImage() {
        this.props.dispatch(commonActions.common.login.setAva(this.state.newImage))
        this.setState(initialState)
    }


    render() {
        switch (this.state.state){
            case STATE.CHANGE:
                return <>
                    <Modal
                        onClose={() => this.setState({
                            state: STATE.BASE,
                        })}
                        style={{
                            display: 'flex',
                            flexDirection: 'column',
                        }}
                    >
                        <div style={{
                            position: 'relative',
                            flexGrow: 1,
                        }}>
                            {/* wild magick
                            // @ts-ignore */}
                            <Cropper
                                image={this.state.image}
                                crop={this.state.crop}
                                zoom={this.state.zoom}
                                aspect={4 / 4}
                                onCropChange={(crop: Point) => this.setState({
                                    crop,
                                })}
                                onCropComplete={(_: Area, area: Area) => this.setState({
                                    newImage: getCroppedImg(this.state.image, area),
                                })}
                                onZoomChange={(zoom: number) => this.setState({
                                    zoom,
                                })}
                            />
                        </div>
                        <Button
                            onClick={() => this.setState({
                                state: STATE.PREVIEW,
                            })}
                            style="action"
                        >
                            Предпросмотр
                        </Button>
                    </Modal>
                </>
            case STATE.PREVIEW:
                return <>
                    <Modal
                        onClose={() => this.setState({
                            state: STATE.BASE,
                        })}
                        style={{
                            display: 'flex',
                            flexDirection: 'column',
                        }}
                    >
                        <div style={{
                            position: 'relative',
                            flexGrow: 1,
                            display: 'flex',
                            justifyContent: 'center',
                            alignItems: 'center',
                        }}>
                            <img
                                src={this.state.newImage}
                            />
                        </div>
                        <Button
                            onClick={() => this.submitImage()}
                            style="action"
                        >
                            Подтвердить
                        </Button>
                    </Modal>
                </>
            case STATE.LOADING:
            case STATE.BASE:
                return <>
                    <input
                        type="file" style={{display: 'none'}}
                        ref={this.inputRef}
                        onChange={e => this.imageChange(e)}
                    />
                    <Edit
                        edit={this.props.login.profile.person_id === this.props.person.person_id}
                        onClick={() => this.inputRef.current.click()}
                    >
                        {
                            this.props.person.avas === undefined || this.props.person.avas.length === 0
                                ? <Incognito width={300} height={300}/>
                                : <img
                                    src={this.props.person.avas[0].ava}
                                    style={{width: 300, height: 300}}
                                />
                        }

                    </Edit>
                </>
        }
    }
}