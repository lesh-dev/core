import * as React from "react"
import {connect, Provider, Store} from "react-redux"
import {applyMiddleware, combineReducers, createStore} from "redux"
import thunkMiddleware from 'redux-thunk'
import { createLogger } from 'redux-logger'
import { composeWithDevTools } from 'redux-devtools-extension'
import { Lens } from "./Search"
import {HighlightTitle} from "./Snippet";
import "../../../scss/exams.scss"



//     _          _
//    / \   _ __ (_)
//   / _ \ | '_ \| |
//  / ___ \| |_) | |
// /_/   \_\ .__/|_|
//         |_|
//


const getExams = (schoolId: number) => fetch(
    `//localhost:3000/school?school_id=eq.${schoolId}\
    &select=school_title,\
    person_school(is_teacher,member_department_id,\
    person(person_id,first_name,last_name,\
    exam(exam_status,exam_id,\
    course(course_id,course_title,course_created,school_id,course_cycle,
        course_teachers(person(first_name,last_name,person_id)) )\
    )))\
    &person_school.person.exam.course.school_id=eq.${schoolId}\
    &person_school.is_teacher=eq.`
        .replace(/ +/g, '')
).then(val => val.json())
 .then((val: Ex[]) => reshape2(val));

// Shape from postgrest
interface Ex {
    school_title: string
    person_school: { // []
        is_teacher: string
        member_department_id: number
        person: {
            person_id: number
            first_name: string
            last_name: string
            exam: { // []
                exam_id: number
                exam_status: string
                course?: {
                    course_id: number
                    course_title: string
                    course_cycle: string
                    course_teachers: { person: {person_id: number,first_name: string,last_name: string} }[]
                }
            }[]
        }
    }[]
}

interface PersonSchoolShape {
    is_teacher: string
    member_department_id: number
    person: PersonInfoShape
}
interface PersonInfoShape {
    person_id: number
    first_name: string
    last_name: string
    exam: ExamShape[]
}


// Reshaped
interface ExamsDataShape {
    school_title: string
    persons: Map<string, PersonShape>
}
type PersonShape = {
    person_id: number
    first_name: string
    last_name: string
    exam: Map<number, ExamShape>
    is_teacher: string
    member_department_id: number
}
interface ExamShape {
    exam_id: number
    exam_status: string
    course?: {
        course_id: number
        course_title: string
        course_cycle: string
    }
}



type Course = {
    course_id: number
    course_title: string
    course_cycle: string
}


function changeExam(student: number, course: number, status?: string, exam_id?: number) {
    const uri = "//localhost:3000/exam";
    const headers = {
        "Content-Type": "application/json",
        "Prefer": "return=representation",
        //"Prefer": "resolution=merge-duplicates"
    }
    let result;
    if(!exam_id) {
        const exam = {
            student_person_id: student,
            course_id: course,
            exam_status: status,
        };
        result = fetch(uri, { method: "POST",
            headers,
            body: JSON.stringify(exam),
        })
    } else if(!!status) {
        result = fetch(uri + "?exam_id=eq." + exam_id, {
            method: "PATCH",
            headers,
            body: JSON.stringify({ exam_status: status }),
        })
    }
    else {
        result = fetch(uri + "?exam_id=eq." + exam_id, {
            method: "DELETE",
            headers,
        })
    }
    return result;
}

function createCourse(course_title: string, course_cycle: string, school_id: number) {
    const uri = "//localhost:3000/course";
    const course = { course_title, course_cycle, school_id };
    return fetch(uri, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Prefer": "return=representation",
        },
        body: JSON.stringify(course),
    }).then(resp => resp.json());
}

type AC = {
    course_id: number
    course_title: string
    course_teachers: { person: { person_id: number, first_name: string, last_name: string } } []
    exam: { exam_id: number, exam_status: string, exam_type?: string /*todo*/ } []
}

function reshapeAutocompletions(courses: AC[]): Map<string, CourseWithExam> {
    const coursesKeys = courses.map(ac => ({['_'+ac.course_id]: { course: reshapeTeachers(ac), exam: ac.exam[0] }})) ;
    return Object.assign({}, ...coursesKeys)
}

// TODO: искать также по авторам курсов
function getCourseAutocompletions(query: string, school_id: number, person_id: number) {
    const uri = `//localhost:3000/course?
        limit=5&
        school_id=eq.${school_id}&
        select=*,exam(*),course_teachers(person(person_id,first_name,last_name))&
        exam.student_person_id=eq.${person_id}`.replace(/ +/g, '')
    const terms = query.split(/ +/);
    const x = uri + terms.map(t => `&course_title=ilike.%${encodeURIComponent(t)}%`).join('')
    return fetch(x).then(resp => resp.json())
        .then(val => reshapeAutocompletions(val as AC[]));
}

function reshapeTeachers(c: any) {
    const {course_teachers, ...rest} = c;
    return {course_teachers: course_teachers.map((p: any) => p.person), ...rest}
}

function reshape2(exams: Ex[]): { exam_table: TableState, school_title: string } {
    const {person_school, ...other} = exams[0];
    function comparator(a: PersonSchoolShape, b: PersonSchoolShape) {
        if(a.member_department_id < b.member_department_id) return -1;
        if(a.member_department_id > b.member_department_id) return +1;
        if(a.person.last_name < b.person.last_name) return -1;
        if(a.person.last_name > b.person.last_name) return +1;
        if(a.person.first_name < b.person.first_name) return -1;
        if(a.person.first_name > b.person.first_name) return +1;
        return 0;
    }
    const personKeys = person_school.sort(comparator)
        .map(p => ({ ['_'+p.person.person_id]: reshapePersonCourses(p) }));
    const persons = Object.assign({}, ...personKeys);

    function reshapePersonCourses(person: PersonSchoolShape): PersonWithCourses {
        const {person: P, is_teacher, ...schoolInfo} = person;
        const {exam, ...personInfo} = P;
        const search = { query: "", result: new Map() };
        return { courses: reshapeExam(exam), person: {...personInfo, ...schoolInfo}, search};
    }
    function reshapeExam(exam: ExamShape[]): Map<string, {exam: Exam, course: Course2}> {
        const examKeys = exam.filter((e:any) => !!e.course).map((e: any) =>
            ({ ['_'+e.exam_id]: { exam: e, course: reshapeTeachers(e.course) } }));
        return Object.assign({}, ...examKeys);
    }
    return { exam_table: persons, ...other }
}


//  ____        _          _____
// |  _ \  __ _| |_ __ _  |_   _|   _ _ __   ___  ___
// | | | |/ _` | __/ _` |   | || | | | '_ \ / _ \/ __|
// | |_| | (_| | || (_| |   | || |_| | |_) |  __/\__ \
// |____/ \__,_|\__\__,_|   |_| \__, | .__/ \___||___/
//                              |___/|_|
//

type Person = {
    person_id: number
    first_name: string
    last_name: string
    member_department_id: number
}

type Course2 = {
    course_id: number
    course_title: string
    course_cycle: string
    course_teachers: Person[]
}

type Exam = {
    exam_id: number
    exam_status: string
    exam_type?: string
    // student_person_id? fixme
    // course_id? fixme
}


// type CourseWithExam = Course2 & { exam?: Exam }
type CourseWithExam = { course: Course2, exam?: Exam }
// type PersonWithCourses = Person & { courses: Map<string, CourseWithExam> }
type PersonWithCourses = {
    person: Person
    courses: Map<string, CourseWithExam>
    search: {
        query: string
        result: Map<string, CourseWithExam>
    }
}

type TableState = Map<string, PersonWithCourses>


//   ____                          ____                      _
//  / ___|___  _   _ _ __ ___  ___/ ___|  ___  __ _ _ __ ___| |__
// | |   / _ \| | | | '__/ __|/ _ \___ \ / _ \/ _` | '__/ __| '_ \
// | |__| (_) | |_| | |  \__ \  __/___) |  __/ (_| | | | (__| | | |
//  \____\___/ \__,_|_|  |___/\___|____/ \___|\__,_|_|  \___|_| |_|
//

type P = { path: string[] }

type ExamFormPresentationStateProps = {
    course: Course2
    exam?: Exam
    student_person_id: number
    selectedStatus: string
    selectedType: string
    changed: () => boolean // selectedStatus == exam.exam_status
}
type ExamFormPresentationCallbackProps = {
    onChange(e: any): void
    onSubmit(student: number, course: Course2, exam: Exam, selectedStatus: string, selectedType: string): void
}
type ExamFormPresentationProps = ExamFormPresentationStateProps & ExamFormPresentationCallbackProps
type ExamFormProps = P & {
    course: Course2
    exam?: Exam
    student_person_id: number
}

const ExamFormPresentation = (props: ExamFormPresentationProps) =>
    <form onChange={props.onChange} onSubmit={e => {
        e.preventDefault();
        props.onSubmit(props.student_person_id, props.course, props.exam, props.selectedStatus, props.selectedType)
    }}>
        <input type={"radio"} name={"selectedStatus"} value={"listen"} checked={props.selectedStatus == "listen"} readOnly={true}/>
        <input type={"radio"} name={"selectedStatus"} value={"passed"} checked={props.selectedStatus == "passed"} readOnly={true}/>
        <input type={"radio"} name={"selectedStatus"} value={"notpassed"} checked={props.selectedStatus == "notpassed"} readOnly={true}/>
        <button disabled={!props.changed()}>{ props.exam ? "change" : "add" }</button>
    </form>
const examFormMapStateToProps = (state: any, ownProps: ExamFormProps) => {
    const exam = ownProps.exam;
    const defaultStatus = exam ? exam.exam_status : "listen";
    const defaultType = exam ? exam.exam_type || "variativ" : "variativ"; // fixme -- declare const
    const {selectedStatus: status, selectedType: type} = Lens.get(state, ownProps.path, {});
    const selectedStatus = status || defaultStatus;
    const selectedType = type || defaultType;
    function changed() {
        const statusChanged = exam ? exam.exam_status == selectedStatus : true;
        const typeChanged = exam ? (exam.exam_type || /*fixme*/ "variativ") == selectedType : true;
        return statusChanged || typeChanged;
    }
    return {
        student_person_id: ownProps.student_person_id,
        course: ownProps.course,
        selectedStatus,
        selectedType,
        changed
    };
}
const examFormMapDispatchToProps = (dispatch: (action: any) => void, ownProps: ExamFormProps) => ({
    onChange: (e: any) => {
        dispatch(examFormChanged({ [e.target.name]: e.target.value }, ownProps.path))
    },
    onSubmit: (student: number, course: Course2, exam: Exam, selectedStatus: string, selectedType: string) => {
        const exam_id = exam ? exam.exam_id : null;
        changeExam(student, course.course_id, selectedStatus, exam_id)
            .then(resp => resp.json()) // todo: update table
            .then((val: Exam[]) => dispatch(examStatusChanged(course, val[0], student, ownProps.path)))
    }
})
const ExamForm = connect(examFormMapStateToProps, examFormMapDispatchToProps)((props: ExamFormPresentationProps) =>
    <ExamFormPresentation {...props}/>)

const EXAM_FORM_CHANGED = "EXAM_FORM_CHANGED";
const examFormChanged = (patch: { status?: string, type?: string }, path: string[]) => ({
    type: EXAM_FORM_CHANGED,
    patch,
    path,
})
const EXAM_STATUS_CHANGED = "EXAM_STATUS_CHANGED";
const examStatusChanged = (course: Course2, exam: Exam, student: number, path: string[]) => ({
    type: EXAM_STATUS_CHANGED,
    course,
    exam,
    student,
    path,
})
const examFormReducer = (state: any, action: any) => {
    switch(action.type) {
        case EXAM_FORM_CHANGED:
            return Lens.localUpdate(state, action.patch, action.path);
        case EXAM_STATUS_CHANGED:
            // we ignore path, fixme
            const path = [action.path[0], '_'+action.student, 'courses', '_'+action.exam.exam_id];
            // fixme: search state does not update
            return Lens.localUpdate(state, { course: action.course, exam: action.exam }, path);
        default:
            return state;
    }
}


const CourseExam = (props: {course: Course2, exam: Exam} & P & { student: number }) => <div>
    <a href={`/admin/gui/course/${props.course.course_id}`}>{ props.course.course_title }</a>
    ({ props.course.course_teachers.map(p => `${p.first_name} ${p.last_name}`).join() })
    <ExamForm path={[...props.path, "exam_form"]}
              course={props.course}
              student_person_id={props.student}
              exam={props.exam}/>
</div>





type CourseSearchPresentationProps = {
    person_id: number
    query: string
    result: Map<string,CourseWithExam>
    onQueryChange(query: string): void
    path: string[]
}

type CourseSearchProps = {
    path: string[]
    school_id: number
    person_id: number
}

const CourseSearchPresentation = (props: CourseSearchPresentationProps) => <div>
    <input value={props.query} onChange={e => props.onQueryChange(e.target.value)}/>
    <ul>
        { Object.values(props.result).map((ac:CourseWithExam) => {
            return <li key={ac.course.course_id}>
                <CourseExam path={[...props.path, 'result', '_'+ac.course.course_id]/*course or exam?*/}
                            course={ac.course}
                            exam={ac.exam}
                            student={props.person_id}
                />
            </li>}
        )}
    </ul>
</div>

const courseSearchMapStateToProps = (state: any, ownProps: CourseSearchProps) => {
    const {query,result} = Lens.get(state, ownProps.path, {query:"", result: []});
    return {query,result,person_id: ownProps.person_id};
}
const courseSearchMapDispatchToProps = (dispatch: (action: any) => void, ownProps: CourseSearchProps) => ({
    onQueryChange: (query: string) => {
        dispatch(courseSearchQueryChanged(query, ownProps.path));
        if(query.trim() == "") {
            dispatch(courseSearchResponse(query, new Map(), ownProps.path));
            return;
        }
        getCourseAutocompletions(query, ownProps.school_id, ownProps.person_id)
            .then(result => dispatch(courseSearchResponse(query, result, ownProps.path)))
    }
})

const CourseSearch = connect(courseSearchMapStateToProps, courseSearchMapDispatchToProps)(props =>
    <CourseSearchPresentation path={props.path}
                              person_id={props.person_id}
                              query={props.query}
                              result={props.result}
                              onQueryChange={props.onQueryChange}/>)

const COURSE_SEARCH_QUERY_CHANGED = "COURSE_SEARCH_QUERY_CHANGED";
const COURSE_SEARCH_RESPONSE = "COURSE_SEARCH_RESPONSE";

const courseSearchQueryChanged = (query: string, path: string[]) => ({
    type: COURSE_SEARCH_QUERY_CHANGED,
    query,
    path,
})

const courseSearchResponse = (query: string, result: Map<string,CourseWithExam>, path: string[]) => ({
    type: COURSE_SEARCH_RESPONSE,
    query,
    result,
    path,
})

const courseSearchReducer = (state: any, action: any) => {
    switch(action.type) {
        case COURSE_SEARCH_QUERY_CHANGED:
            return Lens.localUpdate(state, {query: action.query}, action.path);
        case COURSE_SEARCH_RESPONSE:
            const {query} = Lens.get(state, action.path);
            if(query != action.query) return state;
            return Lens.localUpdate(state, {result: action.result}, action.path);
        default:
            return state;
    }
}


//   ____                _        ____
//  / ___|_ __ ___  __ _| |_ ___ / ___|___  _   _ _ __ ___  ___
// | |   | '__/ _ \/ _` | __/ _ \ |   / _ \| | | | '__/ __|/ _ \
// | |___| | |  __/ (_| | ||  __/ |__| (_) | |_| | |  \__ \  __/
//  \____|_|  \___|\__,_|\__\___|\____\___/ \__,_|_|  |___/\___|
//

// Actions
const COURSE_FILLING_STARTED = "COURSE_FILLING_STARTED";
const COURSE_CREATE_REQUEST = "COURSE_CREATE_REQUEST";
const COURSE_CREATE_RESPONSE = "COURSE_CREATE_RESPONSE";
const COURSE_CREATE_TITLE_CHANGED = "COURSE_CREATE_TITLE_CHANGED";
const COURSE_CREATE_CYCLE_CHANGED = "COURSE_CREATE_CYCLE_CHANGED";

const courseFillingStarted = (path: string[]) => ({
    type: COURSE_FILLING_STARTED,
    path,
});
const courseCreateRequest = (path: string[]) => ({
    type: COURSE_CREATE_REQUEST,
    path,
});
const courseCreateResponse = (course: Course, path: string[]) => ({
    type: COURSE_CREATE_RESPONSE,
    course,
    path,
});
const courseCreateTitleChanged = (title: string, path: string[]) => ({
    type: COURSE_CREATE_TITLE_CHANGED,
    title,
    path,
});
const courseCreateCycleChanged = (cycle: string, path: string[]) => ({
    type: COURSE_CREATE_CYCLE_CHANGED,
    cycle,
    path,
});

// Presentation
const CreateCoursePresentation = (props: any) => <div className={"create-course"}>
    {/*<input type={"text"} placeholder={"название"} value={props.title} onChange={e => props.onTitleChange(e.target.value)}/>*/}
    <input type={"text"}
           placeholder={"цикл"}
           className={"create-course__cycle"}
           value={props.cycle}
           onChange={e => props.onCycleChange(e.target.value)}/>
    <button onClick={() => props.onCreate(props.title, props.cycle, props.school_id)}
            className={"create-course__create"}>
        создать
    </button>
</div>

// Callbacks
interface CreateCourseProps {
    path: string[]
    onCreated(course: Course): void
    school_id: number
    title: string
    cycle?: string
}

const createCourseMapStateToProps = (state: any, ownProps: CreateCourseProps) => {
    const localState = Lens.get(state, ownProps.path, {cycle: ownProps.cycle || ""});
    return {
        title: ownProps.title,
        cycle: localState.cycle,
        school_id: ownProps.school_id
    }
}

const createCourseMapDispatchToProps = (dispatch: (action: any) => void, ownProps: CreateCourseProps) => ({
    onCreate: (course_title: string, course_cycle: string, school_id: number) => {
        dispatch(courseCreateRequest(ownProps.path));
        createCourse(course_title, course_cycle, school_id)
            .then(res => {
                dispatch(courseCreateResponse(res[0], ownProps.path));
                ownProps.onCreated(res[0]);
            })
    },
    onTitleChange: (value: string) => {
        dispatch(courseCreateTitleChanged(value, ownProps.path));
    },
    onCycleChange: (value: string) => {
        dispatch(courseCreateCycleChanged(value, ownProps.path));
    },
})

export const CreateCourse = connect(createCourseMapStateToProps, createCourseMapDispatchToProps)(
    (props: CreateCourseProps) => <CreateCoursePresentation {...props}/>
);

// reducer

const createCourseReducer = (state: any, action: any) => {
    switch(action.type) {
        case COURSE_CREATE_TITLE_CHANGED:
            return Lens.localUpdate(state, {title: action.title}, action.path);
        case COURSE_CREATE_CYCLE_CHANGED:
            return Lens.localUpdate(state, {cycle: action.cycle}, action.path);
        case COURSE_CREATE_REQUEST:
        // todo: disable button
        case COURSE_CREATE_RESPONSE:
        // todo: close button; parent provides callback to select this course
        default: return state;
    }
}


const Status = {
    suggesting: "suggesting",
    pending: "pending",
    filling: "filling",
    creating: "creating",
    selected: "selected"
};





//  _____                   _____     _     _
// | ____|_  ____ _ _ __ __|_   _|_ _| |__ | | ___
// |  _| \ \/ / _` | '_ ` _ \| |/ _` | '_ \| |/ _ \
// | |___ >  < (_| | | | | | | | (_| | |_) | |  __/
// |_____/_/\_\__,_|_| |_| |_|_|\__,_|_.__/|_|\___|
//


// Actions
const LOADED_EXAMS = "LOADED_EXAMS";
const loadedExams = (school_id: number, exams: {exam_table: TableState, school_title: string}, path: string[]) => ({ type: LOADED_EXAMS, school_id, exams, path });

const EXAM_REMOVED = "EXAM_REMOVED";
const examRemoved = (exam_id: number, path: string[]) => ({
    type: EXAM_REMOVED,
    exam_id,
    path
})

interface ExamTableProps {
    exam_table: TableState // fixme should not know about ExamForm states
    school_title: string
    dispatch(action: any): void
    school_id: number
}

// Presentation
class ExamTablePresentation extends React.Component<ExamTableProps> {
    render() {
        const persons = this.props.exam_table || {};
        const school_title = this.props.school_title || "";
        return <div>
            <span className={"exam-table__school-title"}>{ school_title }</span>
            <table className={"exam-table"}><tbody>
            { (Object.values(persons) as PersonWithCourses[]).map(p =>
                [<tr key={p.person.person_id + "_person"} className={"exam-table__person-row"}>
                    <td key={"0"} className={"exam-table__person"}>
                        {p.person.first_name} {p.person.last_name}
                    </td>
                    <td key={"1"} className={"exam-table__add-exam"}>
                        <CourseSearch path={["exam_table", "_"+p.person.person_id, "search"]}
                            person_id={p.person.person_id}
                            school_id={this.props.school_id}/>
                    </td>
                </tr>,
                <tr key={p.person.person_id + "_exam"} className={"exam-table__row"}>
                    { ["1", "2", "3", "4", "5"].map(cycle => {
                        const courses = Object.values(p.courses).filter(e => !!e /* fixme */) as CourseWithExam[];
                        // значение цикла бывает 4-5, 1-3, пустой
                        function cycleOf(course_cycle: string) { return course_cycle.slice(0,1) || "1"; }
                        return <td key={cycle} className={"exam-table__cycle"}>
                            <ul className={"exam-table__courses"}>{
                            courses.filter(e => cycleOf(e.course.course_cycle) == cycle).map(e =>
                                <li key={e.course.course_id} className={"exam-table__course-" + e.exam.exam_status}>
                                    <CourseExam course={e.course}
                                                exam={{exam_id: e.exam.exam_id, exam_status:e.exam.exam_status}}
                                                path={["exam_table", "_"+p.person.person_id, "courses", '_'+e.exam.exam_id]}
                                                student={p.person.person_id}/>
                                </li>
                            ) }</ul>
                        </td>
                    }) }
                </tr>
                ]
            )}
        </tbody></table></div>
    }
    componentDidMount() {
        const dispatch = this.props.dispatch;
        getExams(this.props.school_id)
            .then(exams => dispatch(loadedExams(this.props.school_id, exams,[]) ))
    }
}

// Callbacks
// const etMapStateToProps = ({exams}: ExamTableProps) => ({exams}); // FIXME
const etMapStateToProps = (exams: ExamTableProps) => (exams);
const etMapDispatchToProps = (dispatch: (action: any) => void, ownProps: any) =>({
    dispatch,
});

// Container
const ExamTable = connect(etMapStateToProps, etMapDispatchToProps)(
    (props: ExamTableProps) => <ExamTablePresentation
        school_id={props.school_id}
        school_title={props.school_title}
        exam_table={props.exam_table}
        dispatch={props.dispatch}/>);

// Reducer
const examTableReducer = (state: { exams: ExamsDataShape}, action: any) => {
    switch(action.type) {
        case LOADED_EXAMS:
            return Lens.set(state, action.exams, []);
        case EXAM_REMOVED:
            const prefix = action.path.slice(0,-1);
            return Lens.set(state, { [action.exam_id]: null }, prefix);
        default: return state;
    }
}

//     _    _ _ _____                _   _
//    / \  | | |_   _|__   __ _  ___| |_| |__   ___ _ __
//   / _ \ | | | | |/ _ \ / _` |/ _ \ __| '_ \ / _ \ '__|
//  / ___ \| | | | | (_) | (_| |  __/ |_| | | |  __/ |
// /_/   \_\_|_| |_|\___/ \__, |\___|\__|_| |_|\___|_|
//                        |___/
//


//////////////////////////// store
const reducer = [createCourseReducer, examTableReducer, courseSearchReducer, examFormReducer]
    .reduceRight((f,g) => (state, action) => f(g(state, action), action));

const makeStore = () => createStore(reducer, composeWithDevTools( applyMiddleware(thunkMiddleware, createLogger()) ));

export const ExamsExample = () => <Provider store={makeStore()}><ExamTable school_id={20}/></Provider>