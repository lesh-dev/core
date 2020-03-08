import * as React from 'react'
import {connect} from 'react-redux'
import {ReduxProps} from "../../../redux-structure/store";
import {internalActions, InternalState} from "../../../redux-structure/internal";
import {Edit} from "../../common/Edit";
import {SearchBar} from "../../common/SearchBar";
import {PersonToken} from "../../common/Tokens/PersonToken";
import {CourseTeacherPatch} from "../../../api/internal/course";
import {faTrashAlt} from "@fortawesome/free-regular-svg-icons/faTrashAlt";
import {PatchAction} from "../../../api/internal/common";
import {FontAwesomeIcon as FAIcon} from "@fortawesome/react-fontawesome";
import {Person} from "../../../generated/frontend/interfaces/yasm/database";
import {CommonState} from "../../../redux-structure/common";

enum STATE {
    BASE,
    EDITING,
}



interface TeachersState {
    state: STATE,
    patch: CourseTeacherPatch,
}

@(connect((state: any) => state) as any)
export class Teachers extends React.Component<ReduxProps & {common?: CommonState, internal?: InternalState}, TeachersState>{
    constructor(props: any) {
        super(props)
        this.state = {
            state: STATE.BASE,
            patch: new Map()
        }
    }

    private prepare_changes() {
        return Array(...this.state.patch.entries()).filter(entry => (
            entry[1].action === PatchAction.ADD
        )).map(entry => entry[1].value)
    }

    render_list() {
        switch (this.state.state) {
            case STATE.BASE:
                return <div>
                    {
                        this.props.internal.course.course.teachers.map(ct => <div>
                            <PersonToken person={ct.teacher}/>
                            </div>
                        )
                    }
                </div>
            case STATE.EDITING:
                return <>
                    <table>
                        <tbody>
                        {
                            this.props.internal.course.course.teachers.map(ct => ct.teacher).concat(this.prepare_changes()).filter(person => (
                                    this.state.patch.get(person.id) === undefined || this.state.patch.get(person.id).action !== PatchAction.REMOVE
                                )).map(person => <tr>
                                <td>
                                    <PersonToken person={person}/>
                                </td>
                                <td>
                                    <FAIcon icon={faTrashAlt} onClick={() => {
                                        const patch = this.state.patch
                                        patch.set(person.id, {
                                            value: person,
                                            action: PatchAction.REMOVE,
                                        })
                                        this.setState({
                                            patch: patch,
                                        })
                                    }}/>
                                </td>
                                </tr>
                            )
                        }
                        </tbody>
                    </table>
                    <SearchBar
                        tables={['person']}
                        onClick={(person: Person) => {
                            const patch = this.state.patch
                            patch.set(person.id, {
                                value: person,
                                action: PatchAction.ADD,
                            })
                            if (this.props.internal.course.course.teachers.filter(ct => ct.teacher.id === person.id).length > 0) {
                                patch.delete(person.id)
                            }
                            this.setState({
                                patch: patch,
                            })
                        }}
                        display={person =>
                            <PersonToken person={person}/>
                        }
                    />
                </>
        }
    }

    render() {
        return <Edit
            edit={this.props.internal.course.course.teachers.filter(ct => ct.teacher.id === this.props.common.login.profile.id).length > 0}
            onClick={() =>
                this.setState({state: STATE.EDITING})
            }
            submit={this.state.state === STATE.EDITING}
            onSubmit={() => {
                this.props.dispatch(internalActions.internal.course.patchTeachers(this.props.internal.course.course.id, this.state.patch))
            }}
            exit={this.state.state === STATE.EDITING}
            onExit={() =>
                this.setState({
                    state: STATE.BASE,
                    patch: new Map,
                })
            }
            pad={true}
        >
            {
                this.render_list()
            }
        </Edit>
    }
}