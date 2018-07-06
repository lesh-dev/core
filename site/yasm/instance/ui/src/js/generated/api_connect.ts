import {
    Notification,
    NotificationList,
    Department,
    DepartmentList,
    Person,
    PersonList,
    Course,
    CourseList,
    CourseTeachers,
    CourseTeachersList,
    Exam,
    ExamList,
    School,
    SchoolList,
    PersonSchool,
    PersonSchoolList,
    PersonComment,
    PersonCommentList,
    Submission,
    SubmissionList,
    Contestants,
    ContestantsList,
    Problems,
    ProblemsList,
    Solutions,
    SolutionsList,
} from './interfaces'

import {Promise} from 'es6-promise';

function getRequest(url: string): Promise<any> {
    return new Promise<any>(
        function (resolve, reject) {
            const request = new XMLHttpRequest();
            request.onload = function () {
                if (this.status === 200) {
                    resolve(JSON.parse(this.response));
                } else {
                    reject(new Error(this.statusText));
                }
            };
            request.onerror = function () {
                reject(new Error('XMLHttpRequest Error: ' + this.statusText));
            };
            request.open('GET', url);
            request.send();
        }
    );
}


export function notification_list() {
    return getRequest('/api/notification_list')
}


export function department_list() {
    return getRequest('/api/department_list')
}


export function person_list() {
    return getRequest('/api/person_list')
}


export function course_list() {
    return getRequest('/api/course_list')
}


export function course_teachers_list() {
    return getRequest('/api/course_teachers_list')
}


export function exam_list() {
    return getRequest('/api/exam_list')
}


export function school_list() {
    return getRequest('/api/school_list')
}


export function person_school_list() {
    return getRequest('/api/person_school_list')
}


export function person_comment_list() {
    return getRequest('/api/person_comment_list')
}


export function submission_list() {
    return getRequest('/api/submission_list')
}


export function contestants_list() {
    return getRequest('/api/contestants_list')
}


export function problems_list() {
    return getRequest('/api/problems_list')
}


export function solutions_list() {
    return getRequest('/api/solutions_list')
}


