import * as React from "react";
import * as ReactDOM from "react-dom";
import {Exam, Person, School} from "../generated/interfaces";
import {BasePage} from "./base";
import {connect} from "react-redux";
import {loadProfileOnce, updateExams} from "../redux-structure/api-calls/profile";
import {Table} from "../components/common/Table";
import {SchoolCard} from "../components/common/Cards/SchoolCard";
import {exact} from "prop-types";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faCheck, faTimes, faBook} from "@fortawesome/free-solid-svg-icons";


interface PersonalProps {
    dispatch?: (action: any) => any,
    profile?: Person,
}

@(connect((state: any) => {
    return {profile: state.PROFILE}
}) as any)
class Personal extends React.Component<PersonalProps> {
    constructor(props: PersonalProps) {
        super(props);
    }

    componentWillMount(): void {
        this.props.dispatch(loadProfileOnce)
        this.props.dispatch(updateExams)
    }

    render(): React.ReactNode {
        if (!this.props.profile) {
            return null
        }
        return (
            <Table header={{
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
                            switch (exam.exam_status) {
                                case 'listen':
                                    return <FontAwesomeIcon icon={faBook} color={'orange'}/>
                                case 'passed':
                                    return <FontAwesomeIcon icon={faCheck} color={'green'}/>
                                case 'notpassed':
                                    return <FontAwesomeIcon icon={faTimes} color={'coral'}/>
                            }
                        },
                        sortable: true,
                        sortKey: (exam: Exam) => exam.exam_status,
                        groupable: true,
                        groupKey: (exam: Exam) => exam.exam_status,
                    }
                ]
            }} content={this.props.profile.exam || []}/>
        )
    }
}


ReactDOM.render((
    <BasePage
        page_renderer={() => <Personal/>}
    />
), document.getElementById('mount-point'));
