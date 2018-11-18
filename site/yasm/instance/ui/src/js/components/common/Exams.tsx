import * as React from "react"
import {connect, Provider, Store} from "react-redux"
import {applyMiddleware, combineReducers, createStore} from "redux"
import thunkMiddleware from 'redux-thunk'
import { createLogger } from 'redux-logger'
import { composeWithDevTools } from 'redux-devtools-extension'
import * as nm from "normalizr"
import { Lens } from "./Search"
import {HighlightTitle} from "./Snippet";
import * as _ from "lodash"
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
    exam(exam_status,exam_id,exam_modified,\
    course(course_id,course_title,course_created,school_id,course_cycle,
        course_teachers(person(first_name,last_name,person_id)) )\
    )))\
    &person_school.person.exam.course.school_id=eq.${schoolId}\
    &person_school.is_student=like.%25student`
        .replace(/ +/g, '')
).then(val => val.json())
 .then((val: Ex[]) => normalizeExams(val, schoolId));

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
            exam_modified: "now()", // todo remove me when sql trigger does this work
        };
        result = fetch(uri, { method: "POST",
            headers,
            body: JSON.stringify(exam),
        })
    } else if(!!status) {
        result = fetch(uri + "?exam_id=eq." + exam_id, {
            method: "PATCH",
            headers,
            body: JSON.stringify({
                exam_status: status,
                exam_modified: "now()", /* todo remove me when sql trigger does this work */
            }),
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
        .then(val => reshapeAutocompletions(val as AC[]))
        .then(x => normalizeCourseSearch(x, person_id));
}

function reshapeTeachers(c: any) {
    const {course_teachers, ...rest} = c;
    return {course_teachers: course_teachers.map((p: any) => p.person), ...rest} as Course
}

function normalizeExams(exams: Ex[], school_id: number) {
    const course = new nm.schema.Entity('courses', {}, {idAttribute: 'course_id'})
    const exam = new nm.schema.Entity('exams', { course }, {idAttribute: 'exam_id'})
    const person = new nm.schema.Entity('persons', {exam: [exam]}, {idAttribute: 'person_id'})

    const ps = exams[0].person_school.map(p => p.person)
    const normed = nm.normalize(ps, [person])

    const {entities: {courses, persons, exams:  Exams}, result} = normed;
    const reshapedCourses = Object.assign({}, ...Object.values(normed.entities.courses)
        .map(c => ({ [(c as Course).course_id]: reshapeTeachers(c) })));
    const schools = { [school_id]: { school_title: exams[0].school_title, school_id} };
    const reshapedNormed = { entities: {courses: reshapedCourses, persons, exams: Exams, schools: schools}, result };
    return reshapedNormed;
}

function normalizeCourseSearch(result: Map<string,CourseWithExam>, student: number) {
    const course = new nm.schema.Entity('courses', {}, {idAttribute: 'course_id'})
    const exam = new nm.schema.Entity('exams', {course}, {idAttribute: 'exam_id'})
    const pc = new nm.schema.Entity('person_courses', {course,exam},{idAttribute:(x)=>student+'_'+x.course.course_id})

    const values = Object.values(result);
    const normed = nm.normalize(values,[pc]);
    return normed;
}

function reshape3(exams: ( Person & {exam: (Exam & {course: Course})[] } )[]): TableState {
    const personKeys = exams.sort(comparator)
        .map((p:any) => ({ ['_'+p.person_id]: reshapePerson(p) }));
    const persons = Object.assign({}, ...personKeys);

    function reshapePerson(p: Person & {exam: (Exam & {course: Course})[] }) {
        const {exam: ex, ...personInfo} = p;
        return { person: personInfo, courses: reshapeExam(ex) }
    }
    function reshapeExam(exam: Exam[]): Map<string, {exam: Exam, course: Course}> {
        const examKeys = exam.filter((e:any) => !!e.course).map((e: any) =>
            ({ ['_'+e.exam_id]: { exam: e, course: e.course } }));
        return Object.assign({}, ...examKeys);
    }
    function comparator(a: Person, b: Person) {
        if(a.member_department_id < b.member_department_id) return -1;
        if(a.member_department_id > b.member_department_id) return +1;
        if(a.last_name < b.last_name) return -1;
        if(a.last_name > b.last_name) return +1;
        if(a.first_name < b.first_name) return -1;
        if(a.first_name > b.first_name) return +1;
        return 0;
    }
    return persons;
}

function getExamUpdates(school_id: number, last_modified: string) {
    // todo: member_department_id
    return fetch(`//localhost:3000/exam?select=*,course(*),person(person_id,first_name,last_name)
        &course.school_id=eq.${school_id}&exam_modified=gt.${last_modified}`
        .replace(/ +/g,''))
        .then(response => response.json())
        .then(json => normalizeExamUpdates(json))
}

type EU = {
    entities: {
        courses: Map<number,Course>
        persons: Map<number,Person>
        exams:   Map<number,Exam & { course: number[], person: number[] }>
    }
    result: number[]
}
function normalizeExamUpdates(json: any) {
    const course = new nm.schema.Entity('courses', {}, {idAttribute: 'course_id'});
    const person = new nm.schema.Entity('persons', {}, {idAttribute: 'person_id'});
    const exam = new nm.schema.Entity('exams', {course,person}, {idAttribute: 'exam_id'});


    return nm.normalize(json, [exam]) as EU;
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

type Course = {
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

type School = {
    school_id: number
    school_title: string
}


// type CourseWithExam = Course & { exam?: Exam }
type CourseWithExam = { course: Course, exam?: Exam }
// type PersonWithCourses = Person & { courses: Map<string, CourseWithExam> }
type PersonWithCourses = {
    person: Person
    courses: Map<string, CourseWithExam>
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
    course: Course
    exam?: Exam
    student_person_id: number
}
type ExamFormPresentationCallbackProps = {
    onSubmit(student: number, course: Course, exam: Exam, selectedStatus: string, selectedType: string): void
}
type ExamFormPresentationProps = ExamFormPresentationStateProps & ExamFormPresentationCallbackProps
type ExamFormProps = P & {
    course: Course
    exam?: Exam
    student_person_id: number
}

class ExamFormPresentation extends React.Component<ExamFormPresentationProps, {selectedStatus: string, selectedType: string}> {
    constructor(props: ExamFormPresentationProps) {
        super(props);
        this.state = {
            selectedStatus: props.exam ? props.exam.exam_status : "listen",
            selectedType: props.exam ? props.exam.exam_type || "optional" : "optional",
        }
        this.handleChange = this.handleChange.bind(this);
    }
    render() {
        const props = this.props;
        return <form onChange={this.handleChange} onSubmit={e => {
            e.preventDefault();
            props.onSubmit(props.student_person_id, props.course, props.exam, this.state.selectedStatus, this.state.selectedType)
        }}>
            <div>
                <label title={"listen"}>
                    <input type={"radio"} name={"selectedStatus"} value={"listen"} readOnly={true}
                           checked={this.state.selectedStatus == "listen"}/>
                    ⏿
                </label>
                <label title={"passed"}>
                    <input type={"radio"} name={"selectedStatus"} value={"passed"} readOnly={true}
                           checked={this.state.selectedStatus == "passed"}/>
                    ✅
                </label>
                <label title={"notpassed"}>
                    <input type={"radio"} name={"selectedStatus"} value={"notpassed"} readOnly={true}
                           checked={this.state.selectedStatus == "notpassed"}/>
                    ☠
                </label>
            </div>
            <div>
                <label title={"optional"}>
                    ✪
                    <input type={"radio"} name={"selectedType"} value={"optional"} readOnly={true}
                           checked={this.state.selectedType == "optional"}/>
                </label>
                <label title={"required"}>
                    <input type={"radio"} name={"selectedType"} value={"required"} readOnly={true}
                           checked={this.state.selectedType == "required"}/>
                    ✍
                </label>
                <label title={"facultative"}>
                    <input type={"radio"} name={"selectedType"} value={"facultative"} readOnly={true}
                           checked={this.state.selectedType == "facultative"}/>
                    ❁
                </label>
            </div>
            <button disabled={!this.changed()}>{ props.exam ? "change" : "add" }</button>
        </form>
    }
    handleChange(e: any /*React.FormEvent*/) {
        const target = e.nativeEvent.target; // fixme?
        // const target = e.currentTarget // requires persist()?
        this.setState(state => ({ [target.name]: target.value } as any));
    }
    changed() {
        const statusChanged = this.props.exam ? this.state.selectedStatus != this.props.exam.exam_status : true;
        const typeChanged = this.props.exam ?
            this.state.selectedType != (this.props.exam.exam_type || "optional" /* todo */)
            : true;
        return statusChanged || typeChanged;
    }
}


const examFormMapStateToProps = (state: any, ownProps: ExamFormProps) => {
    return {
        student_person_id: ownProps.student_person_id,
        // а как exam попадает ниже? fixme
        course: ownProps.course,
        path: ownProps.path,
    };
}
const examFormMapDispatchToProps = (dispatch: (action: any) => void, ownProps: ExamFormProps) => ({
    onSubmit: (student: number, course: Course, exam: Exam, selectedStatus: string, selectedType: string) => {
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
const examStatusChanged = (course: Course, exam: Exam, student: number, path: string[]) => ({
    type: EXAM_STATUS_CHANGED,
    course,
    exam,
    student,
    path,
})
const examFormReducer = (state: any, action: any) => {
    switch(action.type) {
        // case EXAM_FORM_CHANGED:
        //     return Lens.localUpdate(state, action.patch, action.path);
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


const CourseExam = (props: {course: Course, exam: Exam} & P & { student: number }) =>
    <div className={"exam-table__course exam-table__course-" + (props.exam ? props.exam.exam_status : "new")}>
    <a href={`/admin/gui/course/${props.course.course_id}`}>{ props.course.course_title }</a>
    <div className={"exam-table__prep"}>({ props.course.course_teachers.map(p => `${p.first_name} ${p.last_name}`).join() })
    </div>
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
    <input className={"exam-table__search-input"} value={props.query} onChange={e => props.onQueryChange(e.target.value)}/>
    <div className={"exam-table__search-answer"}>
        { Object.values(props.result).map((ac:CourseWithExam) => {
            return <div key={ac.course.course_id}>
                <CourseExam path={[...props.path/*, 'result'*/, '_'+ac.course.course_id]/*course or exam?*/}
                            course={ac.course}
                            exam={ac.exam}
                            student={props.person_id}
                />
            </div>}
        )}
    </div>
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
            dispatch(courseSearchResponse(query, new Map(), [], ownProps.person_id, ownProps.path));
            return;
        }
        getCourseAutocompletions(query, ownProps.school_id, ownProps.person_id)
            .then(result => dispatch(courseSearchResponse(query, result.entities, result.result, ownProps.person_id, ownProps.path)))
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

const courseSearchResponse = (query: string, entities: any, result: any, student: number, path: string[]) => ({
    type: COURSE_SEARCH_RESPONSE,
    query,
    entities,
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

            let st = state;
            st = Lens.localUpdate(st, {result: action.result}, action.path);
            st = _.merge({}, st, action.entities);
            return st;
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

const UPDATED_EXAMS = "UPDATED_EXAMS";
const updatedExams = (school_id: number, entities: any) => ({
    type: UPDATED_EXAMS,
    school_id,
    entities,
})


const EXAM_REMOVED = "EXAM_REMOVED";
const examRemoved = (exam_id: number, path: string[]) => ({
    type: EXAM_REMOVED,
    exam_id,
    path
})

interface ExamTablePresentationProps {
    exam_table: TableState
    school_title: string
    school_id: number
}

// Presentation
class ExamTablePresentation extends React.Component<ExamTablePresentationProps> {
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
                            <div className={"exam-table__courses"}>{
                            courses.filter(e => cycleOf(e.course.course_cycle) == cycle).map(e =>
                                <div key={e.course.course_id} className={"exam-table__course-" + e.exam.exam_status}>
                                    <CourseExam course={e.course}
                                                exam={{exam_id: e.exam.exam_id, exam_status:e.exam.exam_status}}
                                                path={["exam_table", "_"+p.person.person_id, "courses", '_'+e.exam.exam_id]}
                                                student={p.person.person_id}/>
                                </div>
                            ) }</div>
                        </td>
                    }) }
                </tr>
                ]
            )}
        </tbody></table></div>
    }
}

type ExamData = {
    courses: Map<number, Course>
    exams: Map<number, Exam>
    persons: Map<number, Person>
    person_courses: Map<string,{course: number, exam?: number}>
    schools: Map<number, School>
    personList: number[] // todo: move
}


const etMapStateToProps = (exams: ExamData, ownProps: any) => {
    if(!exams) return { exam_table: new Map<string,PersonWithCourses>(), school_title: "", school_id: ownProps.school_id }

    const course = new nm.schema.Entity('courses', {}, {idAttribute: 'course_id'})
    const exam = new nm.schema.Entity('exams', { course }, {idAttribute: 'exam_id'})
    const person = new nm.schema.Entity('persons', {exam: [exam]}, {idAttribute: 'person_id'})

    const denorm = nm.denormalize(exams.personList, [person], exams);
    const y = reshape3(denorm);
    const school_title = (exams.schools as any)[ownProps.school_id].school_title; // wtf
    return { exam_table: y, school_id: ownProps.school_id, school_title }
};

const ExamTableRenderer = connect(etMapStateToProps)((props: ExamTablePresentationProps) => <ExamTablePresentation {...props}/>)


const etMapDispatchToProps = (dispatch: (action: any) => void, ownProps: any) =>({
    dispatch,
    school_id: ownProps.school_id,
});


class ExamTableManager extends React.Component<{dispatch(action: any):void, school_id: number}> {
    constructor(props: {dispatch(action: any):void, school_id: number}) {
        super(props);
        this.runRaf = this.runRaf.bind(this);
    }
    render() {
        return <ExamTableRenderer school_id={this.props.school_id}/>
    }
    raf: any = null;
    rafCounter = 0;
    rafRunning = false;
    last_modified = 0;
    componentDidMount() {
        const dispatch = this.props.dispatch;
        getExams(this.props.school_id)
            .then(exams => {
                dispatch(loadedExams(this.props.school_id, exams.entities, exams.result, []) );
                this.last_modified = Object.values(exams.entities.exams)
                    .filter((e: any) => !!e.exam_modified)
                    .map((e: any) => Date.parse(e.exam_modified))
                    .reduce((a,b) => Math.max(a,b), this.last_modified);
                // this.raf = setInterval(() => this.tickUpdate(this.props.school_id), 5000);
                this.rafRunning = true;
                this.raf = requestAnimationFrame(this.runRaf)
            })
    }
    componentWillUnmount() {
        cancelAnimationFrame(this.raf);
        this.rafRunning = false;
    }
    tickUpdate(school_id: number) {
        getExamUpdates(school_id, new Date(this.last_modified + 1 /* because of precision */).toISOString())
            .then(r => {
                if(!this.rafRunning) return; // handle case: response received after unmounting
                r.result.length && this.props.dispatch(updatedExams(this.props.school_id, r.entities));
                this.last_modified = Object.values(r.entities.exams)
                    .filter(e => !!e.exam_modified)
                    .map(e => Date.parse(e.exam_modified))
                    .reduce((a,b) => Math.max(a,b), this.last_modified);
            })
    }
    runRaf() {
        if(this.rafCounter >= 300) {
            this.tickUpdate(this.props.school_id);
            this.rafCounter = 0;
        } else {
            this.rafCounter++;
        }
        if(this.rafRunning) requestAnimationFrame(this.runRaf)
    }
}

const ExamTable = connect(null, etMapDispatchToProps)(
    (props:{school_id: number,dispatch(action: any):void}) =>
        <ExamTableManager school_id={props.school_id} dispatch={props.dispatch}/>)


// Reducer
const examTableReducer = (state: ExamData & { last_modified: number }, action: any) => {
    switch(action.type) {
        case LOADED_EXAMS:
            let st = state;
            //st = Lens.set(st, action.entities, []);
            st = _.merge({}, st, action.entities);
            st = Lens.set(st, { personList: action.personList }, []);
            return st;
        case UPDATED_EXAMS:
            const {courses, persons, exams} = action.entities as EU["entities"];
            const pe = _.groupBy(Object.values(exams), e => e.person);
            const newPersons = Object.keys(pe).map(k => ({ [k]: merge(pe[k], (state.persons as any)[k]) }))
            function merge(newExams: (Exam & {course:number,person:number})[], oldPerson: Person & {exam: number[]}) {
                return Object.assign({}, oldPerson, { exam: _.uniq(
                    [].concat(oldPerson.exam, newExams.map(e=>e.exam_id))
                ) })
            }
            const newEntities= { courses, exams, persons: Object.assign({}, ...newPersons) }
            return _.merge({}, state, newEntities); // TODO: update personList if needed
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

let enhancer: any;
/// #if ENV === "development"
enhancer = composeWithDevTools( applyMiddleware(thunkMiddleware, createLogger()) );
/// #else
enhancer = null;
/// #endif
const makeStore = () => createStore(reducer, enhancer);

export const ExamsExample = () => <Provider store={makeStore()}><ExamTable school_id={20}/></Provider>