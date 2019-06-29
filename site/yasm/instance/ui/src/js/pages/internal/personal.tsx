import * as React from "react";
import {Exam, Person, School} from "../../generated/interfaces";
import {connect} from "react-redux";
import {updateExams} from "../../redux-structure/api-calls/profile";
import {Table} from "../../components/common/Table";
import {SchoolCard} from "../../components/common/Cards/SchoolCard";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faCheck, faTimes, faBook, faQuestion, faClock} from "@fortawesome/free-solid-svg-icons";

interface PersonalProps {
    dispatch?: (action: any) => any,
    profile?: Person,
}

@(connect((state: any) => {
    return {profile: state.PROFILE}
}) as any)
export class Personal extends React.Component<PersonalProps> {
    componentWillMount(): void {
        this.props.dispatch(updateExams)
    }

    render(): React.ReactNode {
        if (!this.props.profile) {
            return null
        }
        return (
            <React.Fragment>
                <Table
                    header={{
                        title: 'ЗачОты',
                        columns: [
                            {
                                title: 'Школа',
                                value: (exam: Exam) => exam.course.school.school_title,
                                groupable: true,
                                groupExtract: (exam: Exam) => exam.course.school,
                                groupKey: (school: School) => school.school_id,
                                groupValue: (school: School) => <SchoolCard school={school}/>
                            },
                            {
                                title: 'Название',
                                value: (exam: Exam) => exam.course.course_title
                            },
                            {
                                title: 'Статус',
                                value: (exam: Exam) => {
                                    let icon = faQuestion
                                    let color = 'black'
                                    switch (exam.exam_status) {
                                        case 'listen':
                                            icon = faBook
                                            color='orange'
                                            break
                                        case 'passed':
                                            icon=faCheck
                                            color='green'
                                            break
                                        case 'notpassed':
                                            icon=faTimes
                                            color='coral'
                                            break
                                    }
                                    return <FontAwesomeIcon icon={icon} color={color} style={{display: 'block', margin: 'auto'}}/>
                                },
                                groupable: true,
                                groupKey: (exam: Exam) => exam.exam_status,
                            }
                        ]
                    }}
                    content={this.props.profile.exam || []}
                />
                <Table
                    header={{
                        title: 'К следующему мероприятию',
                        columns: [
                            {
                                title: '',
                                value: (requirement: any) => {
                                    let icon = faQuestion
                                    let color = 'black'
                                    switch (requirement.status) {
                                        case 'checking':
                                            icon = faClock
                                            color='orange'
                                            break
                                        case 'ok':
                                            icon=faCheck
                                            color='green'
                                            break
                                        case 'wrong':
                                            icon=faTimes
                                            color='coral'
                                            break
                                    }
                                    return <FontAwesomeIcon icon={icon} color={color} style={{display: 'block', margin: 'auto'}}/>
                                },
                            },
                            {
                                title: '',
                                value: (requirement: any) => (
                                    <span>
                                        {requirement.name}
                                    </span>
                                ),
                            }

                        ]
                    }}
                    content={[
                        {
                            status: 'checking',
                            name: 'справка о несудимости',
                            tip: 'пойди и получи в мфц',
                        },
                        {
                            status: 'ok',
                            name: 'паспорт',
                            tip: 'кхэм кхэм',
                        },
                        {
                            status: 'wrong',
                            name: 'медкнижка',
                            tip: 'пойди и получи в Эрисмане',
                        },
                        {
                            status: 'ASD',
                            name: 'ASD',
                            tip: 'asd',
                        },
                    ]}
                />
            </React.Fragment>
        )
    }
}
