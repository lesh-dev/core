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
    course(course_id,course_title,course_created,school_id,course_cycle)\
    )))\
    &person_school.person.exam.course.school_id=eq.${schoolId}\
    &person_school.is_teacher=eq.`
        .replace(/ +/g, '')
).then(val => val.json())
 .then((val: Ex[]) => reshape(val));

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

function reshape(exams: Ex[]): ExamsDataShape {
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
    const personKeys = person_school.sort(comparator).map(p => ({ ['_'+p.person.person_id]: reshapePerson(p) }));
    const persons = Object.assign({}, ...personKeys);
    function reshapePerson(person: PersonSchoolShape) {
        const {person: P, ...schoolInfo} = person;
        const {exam, ...personInfo} = P;
        return { exam: reshapeExam(exam), ...personInfo, ...schoolInfo};
    }
    function reshapeExam(exam: any) {
        const examKeys = exam.filter((e:any) => !!e.course).map((e: any) => ({ [e.exam_id]: e }));
        return Object.assign({}, ...examKeys);
    }
    return { persons, ...other }
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

//   ____                          ___                   _
//  / ___|___  _   _ _ __ ___  ___|_ _|_ __  _ __  _   _| |_
// | |   / _ \| | | | '__/ __|/ _ \| || '_ \| '_ \| | | | __|
// | |__| (_) | |_| | |  \__ \  __/| || | | | |_) | |_| | |_
//  \____\___/ \__,_|_|  |___/\___|___|_| |_| .__/ \__,_|\__|
//                                          |_|
//

interface CourseInputProps {
    query: string
    status: "suggesting" | "pending" | "filling" | "creating" | "selected"
    // suggesting -- пришли результаты поиска, отображаем варианты, курс не выбран
    // pending -- ждём результатов поиска
    // filling -- выбрано "создать новый курс"
    searchResults: Course[]
    selectedCourse?: Course
    school_id: number
    cycle?: string
}
interface CourseInputCallbacks {
    onQueryChange(query: string): void
    onCreate: any
    onSelect(course: Course): void // internal
    onCourseSelect(course: Course): void // external
    onCreated(course: Course): void
    path: string[]
}
const Status = {
    suggesting: "suggesting",
    pending: "pending",
    filling: "filling",
    creating: "creating",
    selected: "selected"
};

// Actions
const COURSE_AUTOCOMPLETE_REQUEST = "COURSE_AUTOCOMPLETE_REQUEST";
const COURSE_AUTOCOMPLETE_RESPONSE = "COURSE_AUTOCOMPLETE_RESPONSE";
export const COURSE_AUTOCOMPLETE_SELECTED = "COURSE_AUTOCOMPLETE_SELECTED"; // предназначается потребителям
const COURSE_AUTOCOMPLETE_CREATE_REQUEST = "COURSE_AUTOCOMPLETE_CREATE_REQUEST";
const COURSE_AUTOCOMPLETE_CREATE_RESPONSE = "COURSE_AUTOCOMPLETE_CREATE_RESPONSE";

const courseAutocompleteRequest = (query: string, path: string[]) =>
    ({ type: COURSE_AUTOCOMPLETE_REQUEST, query, path });
const courseAutocompleteResponse = (query: string, path: string[], result: Course[]) =>
    ({ type: COURSE_AUTOCOMPLETE_RESPONSE, query, path, searchResults: result });
const courseAutocompleteSelected = (course: Course, path: string[]) =>
    ({ type: COURSE_AUTOCOMPLETE_SELECTED, course, path });
const courseAutocompleteCreateRequest = (course_title: string, path: string[]) => // TODO: full MinCourseInfo, MVCourse
    ({ type: COURSE_AUTOCOMPLETE_CREATE_REQUEST, course_title, path });
const courseAutocompleteCreateResponse = (course: Course, path: string[]) =>
    ({ type: COURSE_AUTOCOMPLETE_CREATE_RESPONSE, course, path });

// Presentation
class CourseInputPresentation extends React.Component<CourseInputProps & CourseInputCallbacks> {
    render() {
        return <div className={"course-input"}>
            <input type={"text"} placeholder={"искать"} className={"course-input__search"}
                   value={this.props.query}
                   onChange={e => this.props.onQueryChange(e.target.value)}/>
            {
                this.props.status == Status.selected ?
                    ""
                    :
                    <ul className={"course-input__search-results"}>{
                        this.props.searchResults.map(course =>
                            <li key={course.course_id}
                                className={"course-input__search_result-item"}
                                onClick={() => this.props.onSelect(course)}
                                children={HighlightTitle({query: this.props.query, title: course.course_title})}/>
                        )
                    }</ul>
            }
            или новый курс:
            <CreateCourse school_id={this.props.school_id}
                          path={[...this.props.path, "create_new"]}
                          onCreated={(course) => this.props.onCreated(course)}
                          cycle={this.props.cycle}
                          title={this.props.query}/>
            {
                this.props.status == Status.selected ?
                    <a href={CourseInputPresentation.makeCourseLink(this.props.selectedCourse.course_id)}
                       className={"course-input__selected"}>{
                        this.props.selectedCourse.course_title
                    }</a>
                    :
                    ""
            }
            {/*{ this.props.status === "filling" || this.props.status === "creating" ?*/}
              {/*<button disabled={this.props.status === "creating"}*/}
                      {/*onClick={() => this.props.onCreate(null, null)}>save</button> : ""}*/}
        </div>
    }

    static makeCourseLink(course_id: number) { return `/admin/gui/courses/${course_id}` }
}


// Callbacks

const mapStateToProps = (state: any, ownProps: CourseInputOwnProps) => {
    const localState = Lens.get(state, ownProps.path, initialCourseAutocompleteState);
    const {status, query, searchResults, selectedCourse} = localState;
    return {status, query, searchResults, selectedCourse, cycle: ownProps.cycle, path: ownProps.path, school_id: ownProps.school_id};
}

interface CourseInputOwnProps {
    path: string[];
    onCourseSelect(course: Course): void
    school_id: number
    cycle?: string
}

const mapDispatchToProps = (dispatch: (action: any) => void, ownProps: CourseInputOwnProps) => ({
    onQueryChange: (query: string) => {
        dispatch(courseAutocompleteRequest(query, ownProps.path));
        //const baseUri = "//localhost:3000/search?source=eq.course&limit=5";
        const baseUri = "//localhost:3000/course?limit=5&school_id=eq." + ownProps.school_id;
        const terms = query.split(/\s+/);
        const clauses = terms.map(t => "&course_title=ilike." + encodeURIComponent(`%${t}%`));
        const uri = baseUri + clauses.join('');
        fetch(uri).then(resp => resp.json())
            .then(result => dispatch(courseAutocompleteResponse(query, ownProps.path, result)))
    },
    onCreate: (course_title: string, course_cycle: string) => {
        dispatch(courseAutocompleteCreateRequest(course_title, ownProps.path));
        // TODO: call
        console.log("TODO: add course");
        dispatch(courseAutocompleteCreateResponse({ course_id: -1, course_title, course_cycle }, ownProps.path))
    },
    onSelect: (course: Course) => {
        dispatch(courseAutocompleteSelected(course, ownProps.path))
        ownProps.onCourseSelect(course);
    },
    onCreated: (course: Course) => {
        dispatch(courseAutocompleteSelected(course, ownProps.path));
        ownProps.onCourseSelect(course);
    },
});

// Container
export const CourseInput = connect(mapStateToProps, mapDispatchToProps)(
    //({ onQueryChange, onCreate, query, searchResults, selectedCourse }) =>
    ({...props}) =>
        <CourseInputPresentation {...props} />
);

// Reducer

const initialCourseAutocompleteState = { query: "", status: Status.suggesting, searchResults: ([] as any[]) };

function examAutocompleteReducer(state = {}, action: any) {
    const localState = !!action.path ? Lens.get(state, action.path, initialCourseAutocompleteState) : undefined;
    switch (action.type) {
        case COURSE_AUTOCOMPLETE_REQUEST:
            // обычно синхронное событие, прилетает по изменению квери
            return Lens.localUpdate(state, { status: Status.pending, query: action.query }, action.path, initialCourseAutocompleteState)
        case COURSE_AUTOCOMPLETE_RESPONSE:
            // может прилететь с опозданием, тогда игнорируем
            if(action.query != localState.query || localState.status != Status.pending) return state;
            return Lens.localUpdate(state,
                { status: Status.suggesting, searchResults: action.searchResults },
                action.path,
                initialCourseAutocompleteState);
        case COURSE_AUTOCOMPLETE_CREATE_REQUEST:
            if(localState.status != Status.filling) return state; // вряд ли возможно
            return Lens.localUpdate(state, { status: Status.creating, course_title: action.course_title },
                action.path,
                initialCourseAutocompleteState);
        case COURSE_AUTOCOMPLETE_CREATE_RESPONSE:
            // может прилететь с опозданием тогда игнорируем
            // todo: или лучше всегда использовать? Курс-то создан.
            // TODO: вместо проверки заголовка проверка всех полей
            if(localState.status != Status.creating || localState.course_title != action.course.course_title) return state;
            return Lens.localUpdate(state, {status: Status.selected, selectedCourse: action.course},
                action.path,
                initialCourseAutocompleteState);
        case COURSE_AUTOCOMPLETE_SELECTED:
            return Lens.localUpdate(state, {status: Status.selected, selectedCourse: action.course},
                action.path,
                initialCourseAutocompleteState);
        default: return state;
    }
}



//     _       _     _ _____
//    / \   __| | __| | ____|_  ____ _ _ __ ___
//   / _ \ / _` |/ _` |  _| \ \/ / _` | '_ ` _ \
//  / ___ \ (_| | (_| | |___ >  < (_| | | | | | |
// /_/   \_\__,_|\__,_|_____/_/\_\__,_|_| |_| |_|
//

// Actions
const ADD_EXAM_COURSE_SELECTED = "ADD_EXAM_COURSE_SELECTED";
const addExamCourseSelected = (course: Course, path: string[]) => ({
    type: ADD_EXAM_COURSE_SELECTED,
    path,
    selectedCourse: course
});

const ADD_EXAM_REQUEST = "ADD_EXAM_REQUEST";
const addExamRequest = (exam_status: string, course: Course, student_person_id: number, path: string[]) => ({
    type: ADD_EXAM_REQUEST,
    student_person_id,
    path,
    payload: {
        exam_status,
        course,
    }
})

const ADD_EXAM_RESPONSE = "ADD_EXAM_RESPONSE";
const addExamResponse = (exam_id:number, exam_status: string, course: Course, student_person_id: number, path: string[]) => ({
    type: ADD_EXAM_RESPONSE,
    student_person_id,
    path,
    payload: {
        exam_id,
        exam_status,
        course,
    }
});


// Presentation
const AddExamPresentation = ({onPassed, onListen, onCourseSelect, ...props} :any) => <div className={"add-exam"}>
    <CourseInput path={[...props.path, "course"]} onCourseSelect={onCourseSelect} school_id={props.school_id} cycle={props.cycle}/>
    {
        props.selectedCourse ?
            <span className={"add-exam__buttons"}>
                <button onClick={() => onPassed(props.selectedCourse)}
                        className={"add-exam__passed"}>сдан</button>
                {" "}
                <button onClick={() => onListen(props.selectedCourse)}
                        className={"add-exam__listen"}>прослушан</button>
            </span>
        : ""
    }
</div>

// Callbacks
interface AddExamOwnProps {
    path: string[]
    student: number
    school_id: number
    cycle?: string
}

const initialAddExamState = { selectedCourse: null as any }

const addExamMapStateToProps = (state: any, ownProps: AddExamOwnProps) => {
    const {selectedCourse} = Lens.get(state, ownProps.path, initialAddExamState);
    return {selectedCourse, cycle: ownProps.cycle};
}

const addExamMapDispatchToProps = (dispatch: (action: any) => void, ownProps: AddExamOwnProps) => ({
    onPassed: (course: Course) => {
        dispatch(addExamRequest("passed", course, ownProps.student, ownProps.path));
        changeExam(ownProps.student, course.course_id, "passed")
            .then(resp => resp.json())
            .then(obj =>
                dispatch(addExamResponse(obj[0].exam_id, obj[0].exam_status, course, obj[0].student_person_id, ownProps.path)) )

    },
    onListen: (course: Course) => {
        dispatch(addExamRequest("passed", course, ownProps.student, ownProps.path));
        changeExam(ownProps.student, course.course_id, "listen")
            .then(resp => resp.json())
            .then(obj =>
                dispatch(addExamResponse(obj[0].exam_id, obj[0].exam_status, course, obj[0].student_person_id, ownProps.path)) )

    },
    onCourseSelect: (course: Course | null) => {
        dispatch(addExamCourseSelected(course, ownProps.path))
    },
})

// Container
const AddExam = connect(addExamMapStateToProps, addExamMapDispatchToProps)(({...props}) =>
    <AddExamPresentation {...props}/>
)

// Reducer

function addExamReducer(state = {}, action: any) {
    switch(action.type) {
        case ADD_EXAM_COURSE_SELECTED:
            return Lens.localUpdate(state,
                { selectedCourse: action.selectedCourse},
                action.path);
        case ADD_EXAM_REQUEST:
            return Lens.localUpdate(state, {
                selectedCourse: null,
                status: Status.suggesting
            }, action.path);
        default: return state;
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
const loadedExams = (school_id: number, exams: ExamsDataShape, path: string[]) => ({ type: LOADED_EXAMS, school_id, exams, path });

const EXAM_REMOVED = "EXAM_REMOVED";
const examRemoved = (exam_id: number, path: string[]) => ({
    type: EXAM_REMOVED,
    exam_id,
    path
})

interface ExamTableProps {
    exams: ExamsDataShape
    dispatch(action: any): void
    toggleExamStatus(exam_id: number, old_status: string, person: number, course: Course, path: string[]): void
    removeExam(exam_id: number, path: string[]): void
    school_id: number
}

// Presentation
class ExamTablePresentation extends React.Component<ExamTableProps> {
    render() {
        const persons = !!this.props.exams ? this.props.exams.persons : {};
        const school_title = !!this.props.exams ? this.props.exams.school_title : ""
        return <div>
            <span className={"exam-table__school-title"}>{ school_title }</span>
            <table className={"exam-table"}><tbody>
            { (Object.values(persons) as PersonShape[]).map(person =>
                <tr key={person.person_id} className={"exam-table__row"}>
                    <td key={"0"} className={"exam-table__person"}>
                        {person.first_name} {person.last_name}
                        <AddExam path={["exams", "persons", "_"+person.person_id.toString()]}
                                 student={person.person_id}
                                 school_id={this.props.school_id}/>
                    </td>
                    { ["1", "2", "3", "4", "5"].map(cycle => {
                        const courses = Object.values(person.exam).filter(e => !!e /* fixme */) as ExamShape[];
                        // значение цикла бывает 4-5, 1-3, пустой
                        function cycleOf(course_cycle: string) { return course_cycle.slice(0,1) || "1"; }
                        return <td key={cycle} className={"exam-table__cycle"}>
                            <ul className={"exam-table__courses"}>{
                            courses.filter(e => cycleOf(e.course.course_cycle) == cycle).map(e =>
                                <li key={e.course.course_id} className={"exam-table__course-" + e.exam_status}>
                                    {e.course.course_title}: {e.exam_status}
                                    <button
                                        className={"exam-table__toggle-"+e.exam_status}
                                        onClick={() =>
                                            this.props.toggleExamStatus(
                                                e.exam_id, e.exam_status, person.person_id, e.course,
                                                ["exams", "persons", "_"+person.person_id, "exam", e.exam_id.toString()]
                                            )}>
                                        { e.exam_status == "passed" ? "<" : ">" }
                                    </button>
                                    <button className={"exam-table__remove exam-table__remove-"+e.exam_status}
                                            onClick={() => this.props.removeExam(e.exam_id,
                                                ["exams", "persons", "_"+person.person_id, "exam", e.exam_id.toString()]
                                    )}>x</button>
                                </li>
                            ) }</ul>
                            <AddExam path={["exams", "persons", "_"+person.person_id, cycle]}
                                     student={person.person_id}
                                     cycle={cycle}
                                     school_id={this.props.school_id}/>
                        </td>
                    }) }
                </tr>
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
const etMapStateToProps = ({exams}: ExamTableProps) => ({exams});
const etMapDispatchToProps = (dispatch: (action: any) => void, ownProps: any) =>({
    dispatch,
    toggleExamStatus: (exam_id: number, old_status: string, person: number, course: Course, path: string[]) => {
        const new_status = old_status == "passed" ? "listen" : "passed";
        changeExam(person, course.course_id, new_status, exam_id)
            .then(resp => resp.json())
            .then(val => dispatch(addExamResponse(val[0].exam_id, val[0].exam_status, course, person, path)))
    },
    removeExam: (exam_id: number, path: string[]) => {
        changeExam(null, null, null, exam_id)
            .then(resp => resp.json())
            .then(val => dispatch(examRemoved(exam_id, path)))
    }
});

// Container
const ExamTable = connect(etMapStateToProps, etMapDispatchToProps)(
    (props: ExamTableProps) => <ExamTablePresentation
        school_id={props.school_id}
        exams={props.exams}
        dispatch={props.dispatch}
        removeExam={props.removeExam}
        toggleExamStatus={props.toggleExamStatus} />);

// Reducer
const examTableReducer = (state: { exams: ExamsDataShape}, action: any) => {
    switch(action.type) {
        case LOADED_EXAMS:
            return Lens.set(state, {exams: action.exams}, []);
        case ADD_EXAM_RESPONSE:
            return Lens.set(state, action.payload,
                ["exams", "persons", "_" + action.student_person_id.toString(), "exam", action.payload.exam_id.toString()])
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
const reducer = [addExamReducer, createCourseReducer, examAutocompleteReducer, examTableReducer]
    .reduceRight((f,g) => (state, action) => f(g(state, action), action));

const makeStore = () => createStore(reducer, composeWithDevTools( applyMiddleware(thunkMiddleware, createLogger()) ));

export const ExamsExample = () => <Provider store={makeStore()}><ExamTable school_id={20}/></Provider>