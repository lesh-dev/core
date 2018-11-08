<?php
require_once("${engine_dir}cms/ank/person_school.php");

define('XSM_CT_ALL', 'all');

/**
  * Отдаёт пачку ссылок на преподов текущего курса
  * Формально $school_id можно вытащить из course_id,
  * но так проще жить.
  * @param $course_teacher_id фильтр
  **/
function xsm_get_course_teachers($db, $course_id, $school_id, $course_teacher_id_filter = XSM_CT_ALL)
{
    $teachers_query =
        "SELECT
        tp.first_name, tp.last_name,
        ct.course_teacher_id
        FROM course_teachers ct, person tp WHERE
        (ct.course_id = $course_id) AND
        (tp.person_id = ct.course_teacher_id)
        ORDER BY tp.last_name, tp.first_name";
    $teachers_sel = xdb_query($db, $teachers_query);
    $teachers_ht = "";
    $filtered = ($course_teacher_id_filter == XSM_CT_ALL);
    while ($teachers_data = $teachers_sel->fetchArray(SQLITE3_ASSOC))
    {
        $teacher_fi = xsm_fi_enc($teachers_data);
        $course_teacher_id = $teachers_data['course_teacher_id'];
        if ($course_teacher_id == $course_teacher_id_filter)
            $filtered = true;
        $teacher_link = xsm_person_view_link($course_teacher_id, $school_id, $teacher_fi);
        $teachers_ht .= "$teacher_link ";
    }
    if (!$filtered)
        return false;
    return $teachers_ht;
}

/**
  * Same as previous function, but returns list
  **/
function xsm_get_course_teachers_list($db, $course_id, $school_id)
{
    $teachers_query =
        "SELECT
        tp.first_name, tp.last_name,
        ct.course_teachers_id, ct.course_teacher_id,
        ps.member_department_id, d.department_title
        FROM person tp
        LEFT JOIN course_teachers ct ON (tp.person_id = ct.course_teacher_id)
        LEFT JOIN person_school ps ON (tp.person_id = ps.member_person_id and ps.school_id = $school_id)
        LEFT JOIN department d ON (d.department_id = ps.member_department_id)
        WHERE course_id = $course_id
        ORDER BY tp.last_name, tp.first_name";
    $teachers_sel = xdb_query($db, $teachers_query);
    $course_teachers = array();
    while ($teacher_data = xdb_fetch($teachers_sel)) {
        $course_teachers_id = $teacher_data['course_teachers_id'];
        $course_teachers[$course_teachers_id] = $teacher_data;
    }
    return $course_teachers;
}

function xsm_make_teacher_selector($school_id, $already_added = array())
{
    $attr = '';
    $existance = "(\xE2\x97\x8F)";
    $active = "(\xE2\x97\x8B)";
    return xsm_make_selector_ext('person_id', 'course_teacher_id', XDB_INVALID_ID,
        "##presence# @@last_name@ @@first_name@",
        "SELECT
        person_id, last_name, first_name, '$existance' AS presence
        FROM person_school ps LEFT JOIN person p ON p.person_id = ps.member_person_id
        WHERE
        ps.school_id = $school_id AND LENGTH(ps.is_teacher) > 0

        UNION

        SELECT
        person_id, last_name, first_name, '$active' AS presence
        FROM person p
        WHERE
        p.anketa_status = 'cont' AND LENGTH(p.is_teacher) > 0

        ORDER BY last_name, first_name, presence DESC
        ",
        $attr, $already_added);
}

function xsm_add_course_teacher($course_id, $course_teacher_id)
{
    $course_teachers = array(
        'course_id' => $course_id,
        'course_teacher_id' => $course_teacher_id,
    );

    $res = xdb_insert_or_update(
        'course_teachers',
        array('course_teachers_id' => XDB_NEW),
        $course_teachers,
        xsm_get_fields("course_teachers"));

    // check that this person belongs to given school
    $db = xdb_get();
    $course = xdb_get_entity_by_id('course', $course_id);
    $school_id = $course['school_id'];
    $person_school_id = xsm_get_person_school_id($db, $school_id, $course_teacher_id);
    if ($person_school_id === NULL)
    {
        // and add it if not belongs yet
        $key_name = "person_school_id";
        $teacher = xdb_get_entity_by_id('person', $course_teacher_id);

        $person_school = array(
            'school_id' => $school_id,
            'member_person_id' => $course_teacher_id,
            'is_teacher' => 'teacher',
            'member_department_id' => $teacher['department_id']
        );
        $res = xdb_insert_or_update("person_school", array("person_school_id" => XDB_NEW),
            $person_school, xsm_get_fields("person_school"));
    }
}
?>