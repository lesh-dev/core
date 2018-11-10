import * as React from "react"
import {connect, Provider, Store} from "react-redux"
import {applyMiddleware, combineReducers, createStore} from "redux"
import thunkMiddleware from 'redux-thunk'
import { createLogger } from 'redux-logger'
import { composeWithDevTools } from 'redux-devtools-extension'
import * as nm from "normalizr"
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
 // .then((val: Ex[]) => reshape2(val));

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

function normalizedExams(exams: Ex[]) {
    const course = new nm.schema.Entity('courses', {}, {idAttribute: 'course_id'})
    const exam = new nm.schema.Entity('exams', { course }, {idAttribute: 'exam_id'})
    const person = new nm.schema.Entity('persons', {exam: [exam]}, {idAttribute: 'person_id'})

    const ps = exams[0].person_school.map(p => p.person)
    const normed = nm.normalize(ps, [person])

    const {entities: {courses, persons, exams:  Exams}, result} = normed;
    const reshapedCourses = Object.assign({}, ...Object.values(normed.entities.courses)
        .map(c => ({ [(c as any).course_id]: reshapeTeachers(c) })));
    const reshapedNormed = { entities: {courses: reshapedCourses, persons, exams:  Exams}, result };
    return reshapedNormed;
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
            ({ ['_'+e.exam_id]: { exam: e, course: e.course } }));
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


//  _____                     _____
// | ____|_  ____ _ _ __ ___ |  ___|__  _ __ _ __ ___
// |  _| \ \/ / _` | '_ ` _ \| |_ / _ \| '__| '_ ` _ \
// | |___ >  < (_| | | | | | |  _| (_) | |  | | | | | |
// |_____/_/\_\__,_|_| |_| |_|_|  \___/|_|  |_| |_| |_|
//

type P = { path: string[] }

type ExamFormPresentationStateProps = P & {
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

const ExamFormPresentation = (props: ExamFormPresentationProps) => {
    const baseId = `exam-form-${props.student_person_id}-${props.course.course_id}--${props.path.join('-')}--`;
    return <form onChange={props.onChange} onSubmit={e => {
        e.preventDefault();
        props.onSubmit(props.student_person_id, props.course, props.exam, props.selectedStatus, props.selectedType)
    }}>
        <div>
            <input type={"radio"} name={"selectedStatus"} value={"listen"} readOnly={true}
                   checked={props.selectedStatus == "listen"}
                   id={baseId + 'status-listen'}/>
            <label htmlFor={baseId + 'status-listen'} title={"listen"}>⏿</label>

            <input type={"radio"} name={"selectedStatus"} value={"passed"} readOnly={true}
                   checked={props.selectedStatus == "passed"}
                   id={baseId + 'status-passed'}/>
            <label htmlFor={baseId + 'status-passed'} title={"passed"}>✅</label>

            <input type={"radio"} name={"selectedStatus"} value={"notpassed"} readOnly={true}
                   checked={props.selectedStatus == "notpassed"}
                   id={baseId + 'status-notpassed'}/>
            <label htmlFor={baseId + 'status-notpassed'} title={"notpassed"}>☠</label>
        </div>
        <div>
            <input type={"radio"} name={"selectedType"} value={"optional"} readOnly={true}
                   checked={props.selectedType == "optional"}
                   id={baseId + 'type-optional'}/>
            <label htmlFor={baseId + 'type-optional'} title={"optional"}>✪</label>

            <input type={"radio"} name={"selectedType"} value={"required"} readOnly={true}
                   checked={props.selectedType == "required"}
                   id={baseId + 'type-required'}/>
            <label htmlFor={baseId + 'type-required'} title={"required"}>✍</label>

            <input type={"radio"} name={"selectedType"} value={"facultative"} readOnly={true}
                   checked={props.selectedType == "facultative"}
                   id={baseId + 'type-facultative'}/>
            <label htmlFor={baseId + 'type-facultative'} title={"facultative"}>❁</label>
        </div>
        <button disabled={!props.changed()}>{ props.exam ? "change" : "add" }</button>
    </form>
}


const examFormMapStateToProps = (state: any, ownProps: ExamFormProps) => {
    const exam = ownProps.exam;
    const defaultStatus = exam ? exam.exam_status : "listen";
    const defaultType = exam ? exam.exam_type || "optional" : "optional"; // fixme -- declare const
    const {selectedStatus: status, selectedType: type} = Lens.get(state, ownProps.path, {});
    const selectedStatus = status || defaultStatus;
    const selectedType = type || defaultType;
    function changed() {
        const statusChanged = exam ? exam.exam_status != selectedStatus : true;
        const typeChanged = exam ? (exam.exam_type || /*todo*/ "optional") != selectedType : true;
        return statusChanged || typeChanged;
    }
    return {
        student_person_id: ownProps.student_person_id,
        course: ownProps.course,
        selectedStatus,
        selectedType,
        path: ownProps.path,
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
            .then(resp => resp.json())
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
            let st = state;
            const exam = {...action.exam, course: action.exam.course_id} // fixme -- hack for normalizr workaround
            st = Lens.set(st, exam, ['exams', action.exam.exam_id.toString()]);
            st = Lens.set(st, {}, action.path); // clear selected {status,type} after status change
            // add course to person if needed:
            let exams = state.persons[action.student].exam;
            if(!exams.includes(action.exam.exam_id)) {
                exams = [...exams, action.exam.exam_id];
                st = Lens.localUpdate(st, {exam: exams}, ['persons', action.student.toString()]);
            }
            // update normalized state of search suggestions
            st = Lens.set(st, {exam:action.exam.exam_id,course:action.exam.course_id}, ['person_courses', action.student+'_'+action.exam.course_id]);
            return st;
            // todo: add person if needed
            // we ignore path, fixme
        default:
            return state;
    }
}


//   ____                          ____                      _
//  / ___|___  _   _ _ __ ___  ___/ ___|  ___  __ _ _ __ ___| |__
// | |   / _ \| | | | '__/ __|/ _ \___ \ / _ \/ _` | '__/ __| '_ \
// | |__| (_) | |_| | |  \__ \  __/___) |  __/ (_| | | | (__| | | |
//  \____\___/ \__,_|_|  |___/\___|____/ \___|\__,_|_|  \___|_| |_|
//


const CourseExam = (props: {course: Course2, exam: Exam} & P & { student: number }) =>
    <div className={"exam-table__course-" + (props.exam ? props.exam.exam_status : "new")}>
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
                <CourseExam path={[...props.path/*, 'result'*/, '_'+ac.course.course_id]/*course or exam?*/}
                            course={ac.course}
                            exam={ac.exam}
                            student={props.person_id}
                />
            </li>}
        )}
    </ul>
</div>

const courseSearchMapStateToProps = (state: any, ownProps: CourseSearchProps) => {
    const {query,result:results} = Lens.get(state, ownProps.path, {query:"", result: []});

    const course = new nm.schema.Entity('courses', {}, {idAttribute: 'course_id'})
    const exam = new nm.schema.Entity('exams', {}, {idAttribute: 'exam_id'})
    const pc = new nm.schema.Entity('person_courses', {course,exam},{idAttribute:(x)=>ownProps.person_id+'_'+x.course.course_id})

    const denormed = nm.denormalize(results, [pc], state);

    const result = Object.assign({}, ...denormed
        .map(({course, exam}:{course:any,exam:any}) => ({ ['_'+course.course_id]: { course, exam } }) ))
    return {query,result,person_id: ownProps.person_id};
}
const courseSearchMapDispatchToProps = (dispatch: (action: any) => void, ownProps: CourseSearchProps) => ({
    onQueryChange: (query: string) => {
        dispatch(courseSearchQueryChanged(query, ownProps.path));
        if(query.trim() == "") {
            dispatch(courseSearchResponse(query, new Map(), ownProps.person_id, ownProps.path));
            return;
        }
        getCourseAutocompletions(query, ownProps.school_id, ownProps.person_id)
            .then(result => dispatch(courseSearchResponse(query, result, ownProps.person_id, ownProps.path)))
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

const courseSearchResponse = (query: string, result: Map<string,CourseWithExam>, student: number, path: string[]) => ({
    type: COURSE_SEARCH_RESPONSE,
    query,
    result,
    student,
    path,
})

const courseSearchReducer = (state: any, action: any) => {
    switch(action.type) {
        case COURSE_SEARCH_QUERY_CHANGED:
            return Lens.localUpdate(state, {query: action.query}, action.path);
        case COURSE_SEARCH_RESPONSE:
            const {query} = Lens.get(state, action.path);
            if(query != action.query) return state;

            const student = action.student;

            const course = new nm.schema.Entity('courses', {}, {idAttribute: 'course_id'})
            const exam = new nm.schema.Entity('exams', {course}, {idAttribute: 'exam_id'})
            const pc = new nm.schema.Entity('person_courses', {course,exam},{idAttribute:(x)=>student+'_'+x.course.course_id})

            const values = Object.values(action.result);
            const normed = nm.normalize(values,[pc]);

            let st = state;
            st = Lens.localUpdate(st, {result: normed.result}, action.path);
            st = Lens.localUpdate(st, normed.entities.courses, ['courses']);
            st = Lens.localUpdate(st, normed.entities.exams, ['exams']);
            st = Lens.localUpdate(st, normed.entities.person_courses, ['person_courses']);
            return st;

            return Lens.localUpdate(state, {result: action.result}, action.path);
        default:
            return state;
    }
}




//  _____                   _____     _     _
// | ____|_  ____ _ _ __ __|_   _|_ _| |__ | | ___
// |  _| \ \/ / _` | '_ ` _ \| |/ _` | '_ \| |/ _ \
// | |___ >  < (_| | | | | | | | (_| | |_) | |  __/
// |_____/_/\_\__,_|_| |_| |_|_|\__,_|_.__/|_|\___|
//


// Actions
const LOADED_EXAMS = "LOADED_EXAMS";
const loadedExams = (school_id: number, entities: any, personList: number[], path: string[]) =>
    ({ type: LOADED_EXAMS, school_id, entities, personList, path });

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
            .then((val: Ex[]) => ({normalized: normalizedExams(val)}))
            .then(exams => dispatch(loadedExams(this.props.school_id, exams.normalized.entities, exams.normalized.result, []) ))
    }
}


const etMapStateToProps = (exams: ExamTableProps) => {
    if(!exams) return {}

    const course = new nm.schema.Entity('courses', {}, {idAttribute: 'course_id'})
    const exam = new nm.schema.Entity('exams', { course }, {idAttribute: 'exam_id'})
    const person = new nm.schema.Entity('persons', {exam: [exam]}, {idAttribute: 'person_id'})

    const denorm = nm.denormalize((exams as any).personList, [person], exams);
    const x = [{person_school: denorm.map((person:any) => ({person})), school_title: exams.school_title}];
    const y = reshape2(x)
    return y;
};
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
            let st = state;
            st = Lens.set(st, action.entities, []);
            st = Lens.set(st, { personList: action.personList }, []);
            return st;
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
const reducer = [examTableReducer, courseSearchReducer, examFormReducer]
    .reduceRight((f,g) => (state, action) => f(g(state, action), action));

const makeStore = () => createStore(reducer, composeWithDevTools( applyMiddleware(thunkMiddleware, createLogger()) ));

export const ExamsExample = () => <Provider store={makeStore()}><ExamTable school_id={20}/></Provider>