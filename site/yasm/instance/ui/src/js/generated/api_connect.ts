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

export function getRequest(url: string): Promise<any> {
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


export interface dict {
    [index: string]: string
}



export function notification_list(d: dict = {}) {
    let req = '?';
    for (let key in d) {
        req += key + '=' + d[key] + '&'
    }
    return getRequest('/api/notification_list' + req)
}


export function notification_fill(obj: Notification) {
    return new Promise<Notification>((resolve, reject) => {
        let ans: Notification = obj;
        Promise.all([
             ]
        ).then((values) => {
            resolve(ans);
        }).catch((error) => {
            reject(error);
        })
    })
}


export function department_list(d: dict = {}) {
    let req = '?';
    for (let key in d) {
        req += key + '=' + d[key] + '&'
    }
    return getRequest('/api/department_list' + req)
}


export function department_fill(obj: Department) {
    return new Promise<Department>((resolve, reject) => {
        let ans: Department = obj;
        Promise.all([
                person_list({department_id: String(obj.department_id)}),
                person_school_list({member_department_id: String(obj.department_id)}),
             ]
        ).then((values) => {
            ans.person_list = values[0];
            ans.person_school_list = values[1];
            resolve(ans);
        }).catch((error) => {
            reject(error);
        })
    })
}


export function person_list(d: dict = {}) {
    let req = '?';
    for (let key in d) {
        req += key + '=' + d[key] + '&'
    }
    return getRequest('/api/person_list' + req)
}


export function person_fill(obj: Person) {
    return new Promise<Person>((resolve, reject) => {
        let ans: Person = obj;
        Promise.all([
                course_teachers_list({course_teacher_id: String(obj.person_id)}),
                exam_list({student_person_id: String(obj.person_id)}),
                person_school_list({member_person_id: String(obj.person_id)}),
                person_comment_list({blamed_person_id: String(obj.person_id)}),
             ]
        ).then((values) => {
            ans.course_teachers_list = values[0];
            ans.exam_list = values[1];
            ans.person_school_list = values[2];
            ans.person_comment_list = values[3];
            resolve(ans);
        }).catch((error) => {
            reject(error);
        })
    })
}


export function course_list(d: dict = {}) {
    let req = '?';
    for (let key in d) {
        req += key + '=' + d[key] + '&'
    }
    return getRequest('/api/course_list' + req)
}


export function course_fill(obj: Course) {
    return new Promise<Course>((resolve, reject) => {
        let ans: Course = obj;
        Promise.all([
                course_teachers_list({course_id: String(obj.course_id)}),
                exam_list({course_id: String(obj.course_id)}),
             ]
        ).then((values) => {
            ans.course_teachers_list = values[0];
            ans.exam_list = values[1];
            resolve(ans);
        }).catch((error) => {
            reject(error);
        })
    })
}


export function course_teachers_list(d: dict = {}) {
    let req = '?';
    for (let key in d) {
        req += key + '=' + d[key] + '&'
    }
    return getRequest('/api/course_teachers_list' + req)
}


export function course_teachers_fill(obj: CourseTeachers) {
    return new Promise<CourseTeachers>((resolve, reject) => {
        let ans: CourseTeachers = obj;
        Promise.all([
             ]
        ).then((values) => {
            resolve(ans);
        }).catch((error) => {
            reject(error);
        })
    })
}


export function exam_list(d: dict = {}) {
    let req = '?';
    for (let key in d) {
        req += key + '=' + d[key] + '&'
    }
    return getRequest('/api/exam_list' + req)
}


export function exam_fill(obj: Exam) {
    return new Promise<Exam>((resolve, reject) => {
        let ans: Exam = obj;
        Promise.all([
             ]
        ).then((values) => {
            resolve(ans);
        }).catch((error) => {
            reject(error);
        })
    })
}


export function school_list(d: dict = {}) {
    let req = '?';
    for (let key in d) {
        req += key + '=' + d[key] + '&'
    }
    return getRequest('/api/school_list' + req)
}


export function school_fill(obj: School) {
    return new Promise<School>((resolve, reject) => {
        let ans: School = obj;
        Promise.all([
                person_school_list({school_id: String(obj.school_id)}),
                person_comment_list({school_id: String(obj.school_id)}),
             ]
        ).then((values) => {
            ans.person_school_list = values[0];
            ans.person_comment_list = values[1];
            resolve(ans);
        }).catch((error) => {
            reject(error);
        })
    })
}


export function person_school_list(d: dict = {}) {
    let req = '?';
    for (let key in d) {
        req += key + '=' + d[key] + '&'
    }
    return getRequest('/api/person_school_list' + req)
}


export function person_school_fill(obj: PersonSchool) {
    return new Promise<PersonSchool>((resolve, reject) => {
        let ans: PersonSchool = obj;
        Promise.all([
             ]
        ).then((values) => {
            resolve(ans);
        }).catch((error) => {
            reject(error);
        })
    })
}


export function person_comment_list(d: dict = {}) {
    let req = '?';
    for (let key in d) {
        req += key + '=' + d[key] + '&'
    }
    return getRequest('/api/person_comment_list' + req)
}


export function person_comment_fill(obj: PersonComment) {
    return new Promise<PersonComment>((resolve, reject) => {
        let ans: PersonComment = obj;
        Promise.all([
             ]
        ).then((values) => {
            resolve(ans);
        }).catch((error) => {
            reject(error);
        })
    })
}


export function submission_list(d: dict = {}) {
    let req = '?';
    for (let key in d) {
        req += key + '=' + d[key] + '&'
    }
    return getRequest('/api/submission_list' + req)
}


export function submission_fill(obj: Submission) {
    return new Promise<Submission>((resolve, reject) => {
        let ans: Submission = obj;
        Promise.all([
             ]
        ).then((values) => {
            resolve(ans);
        }).catch((error) => {
            reject(error);
        })
    })
}


export function contestants_list(d: dict = {}) {
    let req = '?';
    for (let key in d) {
        req += key + '=' + d[key] + '&'
    }
    return getRequest('/api/contestants_list' + req)
}


export function contestants_fill(obj: Contestants) {
    return new Promise<Contestants>((resolve, reject) => {
        let ans: Contestants = obj;
        Promise.all([
                solutions_list({contestant_id: String(obj.contestants_id)}),
             ]
        ).then((values) => {
            ans.solutions_list = values[0];
            resolve(ans);
        }).catch((error) => {
            reject(error);
        })
    })
}


export function problems_list(d: dict = {}) {
    let req = '?';
    for (let key in d) {
        req += key + '=' + d[key] + '&'
    }
    return getRequest('/api/problems_list' + req)
}


export function problems_fill(obj: Problems) {
    return new Promise<Problems>((resolve, reject) => {
        let ans: Problems = obj;
        Promise.all([
                solutions_list({problem_id: String(obj.problems_id)}),
             ]
        ).then((values) => {
            ans.solutions_list = values[0];
            resolve(ans);
        }).catch((error) => {
            reject(error);
        })
    })
}


export function solutions_list(d: dict = {}) {
    let req = '?';
    for (let key in d) {
        req += key + '=' + d[key] + '&'
    }
    return getRequest('/api/solutions_list' + req)
}


export function solutions_fill(obj: Solutions) {
    return new Promise<Solutions>((resolve, reject) => {
        let ans: Solutions = obj;
        Promise.all([
             ]
        ).then((values) => {
            resolve(ans);
        }).catch((error) => {
            reject(error);
        })
    })
}


