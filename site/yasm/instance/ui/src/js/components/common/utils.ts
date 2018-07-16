import moment = require("moment");
import {Moment} from "moment";
import {Person} from "../../generated/interfaces";
import {Promise} from "es6-promise";

export function str_2_date_format(s: string) {
    return s.replace(/[.]/g, "-") + "T09:00:00.000Z"
}

export function str_2_date(s: string) {
    if (s)
        return moment(str_2_date_format(s));
    return null
}

export function date_2_str(m: Moment) {
    if (m)
        return "" + m.format("YYYY.MM.DD");
    return null
}

export function ava_small(p: Person) {
    return new Promise<string>((resolve, reject) => {
            resolve("/static/emblems/people/incognito.jpg")
        }
    )
}

export function ava_big(p: Person) {
    return new Promise<string>((resolve, reject) => {
            resolve("/static/emblems/people/incognito.jpg")
        }
    )
}

export function redirect(url: string) {
    location.href = url
}