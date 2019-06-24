import * as _ from 'lodash';
import axios, {AxiosResponse} from 'axios';
import {Exam, Person} from "../../../generated/interfaces";
import {profileLoaded, profileUpdated} from "../../actions/profile";

function get_profile() {
    return fetch('/personal/get_profile').then(resp => resp.json()) // TODO: fetch -> axios
}

function get_exams(person_id: number) {
    return axios.request({
        maxRedirects: 0,
        method: 'get',
        url: `/postgrest/exam?
        student_person_id=eq.${person_id}&
        select=*,
        course(
            course_title,
            course_cycle,
            course_type,
            course_area,
            school(
                school_title,
                school_type
            )
        )`.replace(/ +/g, ''),
    }).then(response => response.data)
}

let profile_loader = undefined as any;

export function loadProfileOnce(dispatch: (action: any) => any, getState: any) {
    if (profile_loader === undefined) {
        profile_loader = get_profile().then(value =>
            dispatch(profileLoaded(value))
        )
        return profile_loader
    } else {
        return profile_loader
    }

}

export function updateProfile(state: Person, dispatch: (action: any) => any): Promise<any> {
    return get_profile().then(value => {
        dispatch(profileUpdated(value));
    })
}

export function updateExams(dispatch: (action: any) => any, getState: any) {
    return dispatch(loadProfileOnce).then(() =>
        get_exams(getState().PROFILE.person_id).then((value: Exam[]) =>
            dispatch(profileUpdated({exam: value} as Person))
        )
    )
}
