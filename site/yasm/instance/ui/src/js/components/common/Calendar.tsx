import * as React from "react"
import {connect, Provider, Store} from "react-redux"
import {applyMiddleware, combineReducers, createStore} from "redux"
import thunkMiddleware from 'redux-thunk'
import {createLogger} from 'redux-logger'
import {composeWithDevTools} from 'redux-devtools-extension'
import * as nm from "normalizr"
import {Lens} from "./Search"
import {HighlightTitle} from "./Snippet";
import * as _ from "lodash"
import "../../../scss/exams.scss"
import {schema} from "normalizr";


//     _          _
//    / \   _ __ (_)
//   / _ \ | '_ \| |
//  / ___ \| |_) | |
// /_/   \_\ .__/|_|
//         |_|
//

const getCalendar = (schoolId: number) => fetch(
    `/postgrest/person_school?\
    select=*,\
        person(*),\
        calendar(*)\
    &school_id=eq.${schoolId}`
        .replace(/ +/g, '')
).then(val => val.json());

// Shape from postgrest
interface Calendar {
    person_school_id: number
    person: {
        person_id: number
        first_name: string
        last_name: string
    }
    calendar: {
        date: string
        status: string
    }[]
}

const getDates = (schoolId: number) => fetch(
    `/api/school_dates/${schoolId}`
).then(val => val.json());

type Dates = string[];


//                                 _        _   _
//  _ __  _ __ ___  ___  ___ _ __ | |_ __ _| |_(_) ___  _ __
// | '_ \| '__/ _ \/ __|/ _ \ '_ \| __/ _` | __| |/ _ \| '_ \
// | |_) | | |  __/\__ \  __/ | | | || (_| | |_| | (_) | | | |
// | .__/|_|  \___||___/\___|_| |_|\__\__,_|\__|_|\___/|_| |_|
// |_|
//

interface CalendarProps {
    dates: Dates,
    calendar: Calendar[]
}

export class CalendarPresentation extends React.Component<CalendarProps> {
    render() {
        return <table>
            <thead>
            <tr>
                <td></td>
                {this.props.dates.map((row) => {
                    return <td>
                        {row}
                    </td>
                })}
            </tr>
            </thead>
            <tbody>
            {this.props.calendar.map((row) => {
                return <tr>
                    <td>
                        {row.person.first_name + " " + row.person.last_name}
                    </td>
                    {this.props.dates.map((date) => {
                        return <td>
                            {(row.calendar.find(x => x.date == date) || {status: '?'}).status}
                        </td>
                    })}
                </tr>
            })}
            </tbody>
        </table>
    }
}

interface CalendarManagerProps {
    dispatch(action: any): void,

    school_id: number,
    calendar: Calendar[]
    dates: Dates
}

class CalendarManager extends React.Component<CalendarManagerProps> {
    constructor(props: CalendarManagerProps) {
        super(props);
    }

    render() {
        return <CalendarPresentation dates={this.props.dates} calendar={this.props.calendar}/>
    }

    componentDidMount() {
        const dispatch = this.props.dispatch;
        getCalendar(this.props.school_id).then((response) => {
            dispatch(loadedCalendar(response))
        })
        getDates(this.props.school_id).then((response) => {
            dispatch(loadedDates(response))
        })
    }
}

const calendarMapDispatchToProps = (dispatch: (action: any) => void, ownProps: any) => ({
    dispatch,
    school_id: ownProps.school_id,
});

const calendarMapStateToProps = (state: any) => ({
    calendar: (state || {calendar: []}).calendar || [],
    dates: (state || {dates: []}).dates || []
});

const Calendar = connect(
    calendarMapStateToProps,
    calendarMapDispatchToProps
)((props: any) => < CalendarManager {...props}/>);

//             _   _
//   __ _  ___| |_(_) ___  _ __  ___
//  / _` |/ __| __| |/ _ \| '_ \/ __|
// | (_| | (__| |_| | (_) | | | \__ \
//  \__,_|\___|\__|_|\___/|_| |_|___/
//

const LOADED_CALENDAR = "LOADED_CALENDAR";

const loadedCalendar = (calendar: Calendar[]) => ({
    type: LOADED_CALENDAR,
    calendar
});

const LOADED_DATES = "LOADED_DATES";

const loadedDates = (dates: Dates) => ({
    type: LOADED_DATES,
    dates
});

//               _
//  _ __ ___  __| |_   _  ___ ___ _ __
// | '__/ _ \/ _` | | | |/ __/ _ \ '__|
// | | |  __/ (_| | |_| | (_|  __/ |
// |_|  \___|\__,_|\__,_|\___\___|_|
//

const reducer = (state: any, action: any) => {
    switch (action.type) {
        case LOADED_CALENDAR:
            return Object.assign({}, state, {calendar: action.calendar});
        case LOADED_DATES:
            return Object.assign({}, state, {dates: action.dates});
        default:
            return state
    }
};

//     _    _ _ _____                _   _
//    / \  | | |_   _|__   __ _  ___| |_| |__   ___ _ __
//   / _ \ | | | | |/ _ \ / _` |/ _ \ __| '_ \ / _ \ '__|
//  / ___ \| | | | | (_) | (_| |  __/ |_| | | |  __/ |
// /_/   \_\_|_| |_|\___/ \__, |\___|\__|_| |_|\___|_|
//                        |___/
//

let enhancer: any;
/// #if ENV === "development"
enhancer = composeWithDevTools(applyMiddleware(thunkMiddleware, createLogger()));
/// #else
enhancer = null;
/// #endif
const makeStore = () => createStore(reducer, enhancer);

export const CalendarExample = () => <Provider store={makeStore()}><Calendar school_id={20}/></Provider>