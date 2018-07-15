import moment = require("moment");
import {Moment} from "moment";
import {Person} from "../../generated/interfaces";

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

export function vk_ava_small(p: Person) {
    return "/static/emblems/people/incognito.jpg"
    return "https://pp.userapi.com/c637326/v637326823/30fa3/JdGgrv7ZMxo.jpg?ava=1"
}

export function vk_ava_big(p: Person) {
    return "/static/emblems/people/incognito.jpg"
    return "https://pp.userapi.com/c637326/v637326823/30fa0/By94QoUuQQs.jpg?ava=1"
}

export function redirect(url: string) {
    location.href = url
}