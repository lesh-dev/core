import moment = require("moment");
import {Moment} from "moment";

export function str_2_date(s: string) {
    console.log(s);
    if (s)
        return moment(s.replace(/[.]/g, "-"))
    return null
}

export function date_2_str(m: Moment) {
    if (m)
        return "" + m.year() + "." + m.month() + "." + m.day()
    return null
}