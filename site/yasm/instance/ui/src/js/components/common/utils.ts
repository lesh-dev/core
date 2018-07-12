import moment = require("moment");
import {Moment} from "moment";

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