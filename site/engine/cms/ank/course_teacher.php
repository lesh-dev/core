<?php
require_once("${engine_dir}cms/ank/person_school.php");

function xsm_make_teacher_selector($school_id, $already_added = array())
{
    $attr = '';
    return xsm_make_selector_ext('person_id', 'course_teacher_id', XDB_INVALID_ID,
        "@@last_name@ @@first_name@",
        "SELECT
        person_id, last_name, first_name
        FROM person_school ps LEFT JOIN person p ON p.person_id = ps.member_person_id
        WHERE
        ps.school_id = $school_id AND LENGTH(ps.is_teacher) > 0

        UNION

        SELECT
        person_id, last_name, first_name
        FROM person p
        WHERE
        p.anketa_status = 'cont' AND LENGTH(p.is_teacher) > 0

        ORDER BY last_name, first_name
        ",
        $attr, $already_added);
}

function xsm_add_course_teacher($course_id, $course_teacher_id)
{
    $course_teachers = array(
        'course_id'=>$course_id,
        'course_teacher_id'=>$course_teacher_id
    );

    // TODO: Add some error handling (and duplicate handling also)
    $res = xdb_insert_or_update(
        'course_teachers',
        array('course_teachers_id'=>XDB_NEW),
        $course_teachers,
        xsm_get_course_teachers_fields());

    // ensure that this person belongs to given school
    $db = xdb_get();
    $course = xdb_get_entity_by_id('course', $course_id);
    $school_id = $course['school_id'];
    $person_school_id = xsm_get_person_school_id($db, $school_id, $course_teacher_id);
    if ($person_school_id === NULL)
    {
        $key_name = "person_school_id";
        $teacher = xdb_get_entity_by_id('person', $course_teacher_id);

        // TODO: call person_school API here
        $person_school = array(
            'school_id'=>$school_id,
            'member_person_id'=>$course_teacher_id,
            'is_teacher'=>'teacher',
            'member_department_id'=>$teacher['department_id']
        );
        $res = xdb_insert_or_update("person_school", array("person_school_id"=>XDB_NEW),
            $person_school, xsm_get_person_school_fields());
    }
}
?>