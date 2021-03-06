import moment = require("moment");
import {Moment} from "moment";
import {Person} from "../../generated/frontend/interfaces/yasm/database";
//import {Promise} from "es6-promise";

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

export function redirect(url: string) {
    location.href = url
}