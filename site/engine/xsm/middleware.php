<?php

define('XSM_SORT_DIRECTION_ASC', 'ASC');
define('XSM_SORT_DIRECTION_DESC', 'DESC');

/**
  * Посылатор анкет (вынесен сюда, чтобы не затмевать суть дела)
  **/
function xsm_send_anketa($mail_group, $mail_msg, $full_name, $email, $anketa_mode, $manager_mode = false)
{
    if (!xcms_mailer_enabled()) // disabled mailer is not an error
        return true;

    $host = xcms_hostname();
    $subject = "[xsm][$host][$anketa_mode] Новая анкета: $full_name";

    $addr_from = "reg@fizlesh.ru"; // TODO: remove this spike
    $name_from = "FizLesh Notificator";
    $mailer = xcms_get_mailer($addr_from, $name_from);

    // no mails is a success
    if (!xcms_add_mail_group($mailer, $mail_group))
        return true;

    $full_name_tr = xu_transliterate($full_name);
    if ($manager_mode && xu_not_empty($email))
        $mailer->AddReplyTo($email, $full_name_tr);
    else
        $mailer->AddReplyTo($addr_from, $name_from);
    return xcms_mailer_send($mailer, $subject, $mail_msg);
}

/**
 * Посылатор автоответов
**/
function xsm_send_autoreply($mail_msg, $addr_list_to, $reply_to = "", $reply_to_name = "", $subject = "")
{
    if (!xcms_mailer_enabled())
    {
        // disabled mailer is not an error
        return true;
    }

    $subject = "(Lesh) Registration completed!";
    $addr_from = "reg@fizlesh.ru"; // TODO: remove this spike
    $name_from = "FizLesh Notificator";
    $mailer = xcms_get_mailer($addr_from, $name_from);
    foreach ($addr_list_to as $email)
    {
        $mailer->AddAddress($email);
    }
    $mailer->AddReplyTo($reply_to, $reply_to_name);
    return xcms_mailer_send($mailer, $subject, $mail_msg);
}


function xsm_get_city_class($school_city)
{
    $class = "";
    if (xu_empty($school_city))
        $class = "";
    elseif (strpos($school_city, "МО") !== false)
        $class = "not-msk-city";
    elseif (strpos($school_city, "Моск") === false)
        $class = "far-city";
    elseif (strpos($school_city, "Москва") === false)
        $class = "not-msk-city";
    return $class;
}

/**
  * Получение дефолтной школы (самой последней по времени)
  * @return school id (or @c XDB_INVALID_ID in case of empty schools list)
  **/
function xsm_get_default_school()
{
    $db = xdb_get();
    $query = "SELECT school_id FROM school ORDER BY school_date_start DESC LIMIT 1";
    $school_sel = xdb_query($db, $query);
    if ($school = xdb_fetch($school_sel)) {
        return $school['school_id'];
    }

    echo "Warning: NO SCHOOLS FOUND AT ALL<br />";
    return XDB_INVALID_ID;
}

/**
  * Получение дефолтной школы с учётом текущего контекста запроса
  **/
function xsm_get_default_school_from_request()
{
    $default_school_id = xsm_get_default_school();
    $school_id = xcms_get_key_or($_GET, 'school_id', $default_school_id);
    if ($school_id == XSM_SCHOOL_ANK_ID)
        $school_id = $default_school_id;
    return $school_id;
}

/**
  * Получение id школы по имени
  * @return school id (or XDB_INVALID_ID when not found)
  **/
function xsm_get_school_by_title($school_title)
{
    $db = xdb_get();
    $query = "SELECT school_id FROM school WHERE school_title = '$school_title'";
    $school_sel = xdb_query($db, $query);
    if ($school = xdb_fetch($school_sel)) {
        return $school['school_id'];
    }

    return XDB_INVALID_ID;
}

/**
  * Отдаёт список из курсов текущей школы и связанных с ними объектов.
  * @param $school_id ID школы
  **/
function xsm_get_all_course_info($db, $school_id)
{
    $courses_query = "SELECT
        course_id, course_title
        FROM course WHERE school_id = '$school_id'
        ORDER BY course_title";
    $courses_sel = xdb_query($db, $courses_query);
    $courses = array();
    while ($course = xdb_fetch($courses_sel)) {
        $course_id = $course['course_id'];
        $course['teachers'] = array();
        $courses[$course_id] = $course;
    }

    $teachers_query =
        "SELECT
        ct.course_id, ct.course_teacher_id,
        tp.first_name, tp.last_name
        FROM course_teachers ct, person tp, course c WHERE
        (tp.person_id = ct.course_teacher_id) AND
        (c.school_id = '$school_id') AND
        (ct.course_id = c.course_id)
        ORDER BY tp.last_name, tp.first_name";
    $teachers_sel = xdb_query($db, $teachers_query);
    while ($teachers_data = xdb_fetch($teachers_sel)) {
        $course_id = $teachers_data['course_id'];
        $course_teacher_id = $teachers_data['course_teacher_id'];
        $courses[$course_id]['teachers'][$course_teacher_id] = $teachers_data;
    }
    return $courses;
}


function xsm_get_separated_schools($db, $query, $current_school_id)
{
    $school_sel = xdb_query($db, $query);
    $shown_schools = array();
    $older_schools = array();
    $is_current_school_visible = false;
    $current_school = false;
    while ($school = xdb_fetch($school_sel)) {
        if ($school["school_id"] == $current_school_id) {
            $current_school = $school;
        }

        if (count($shown_schools) <= XSM_SCHOOL_COUNT) {
            $shown_schools[] = $school;
            if ($school["school_id"] == $current_school_id) {
                $is_current_school_visible = true;
            }
        } else {
            $older_schools[] = $school;
        }
    }

    if (!$is_current_school_visible && $current_school !== false) {
        $removed_school = array_pop($shown_schools);
        $shown_schools[] = $current_school;
        array_unshift($older_schools, $removed_school);
    }

    return array(
        "shown_schools" => $shown_schools,
        "older_schools" => $older_schools,
    );
}


/**
  * Печать всех школ (селектор сверху)
  * @sa xsm_print_person_schools
  **/
function xsm_print_recent_schools($db, $current_school_id, $table_name)
{
    $query = "SELECT * FROM school ORDER BY school_date_start DESC";
    $separated_schools = xsm_get_separated_schools($db, $query, $current_school_id);
    // do not escape here, will be used in JS string
    $href_prefix = "list-$table_name&school_id=";
    ?>
    <table class="ankList table table-bordered table-condensed"><tr>
        <?php
        foreach ($separated_schools["shown_schools"] as $school)
        {
            $href = htmlspecialchars("$href_prefix${school['school_id']}");
            $title = htmlspecialchars($school['school_title']);
            $active = ($school["school_id"] == $current_school_id) ? "current" : ""; ?>
            <td class="school-selection <?php echo $active; ?>"><a
                href="<?php echo $href; ?>"><?php echo $title; ?></a></td>
            <?php
        }
        ?>
        <td class="school-selection" style="padding: 4px 8px">
            <select name="view-school" id="view-school-selector" style="padding: 0px; margin: 0px;">
            <?php
            foreach ($separated_schools["older_schools"] as $school)
            {
                $school_id = $school["school_id"];
                $title = xcms_get_key_or_enc($school, "school_title");
                $selected = ($school_id == $current_school_id) ? 'selected="selected"' : '';
                echo "<option $selected value=\"$school_id\">$title</option>\n";
            }
            ?></select>
        </td>
    </tr></table>
    <script>
        $('#view-school-selector').change(function() {
            var val = $('#view-school-selector').val();
            window.location = <?php echo "\"$href_prefix\""; ?> + val;
        });
    </script>
    <?php
}

/**
 * Parse serialized representation of a column sorting order
 * from string like "A,-B,C" to array of dicts "name", "direction".
 */
function xsm_parse_sort_columns($sort_columns_str)
{
    $sort_columns = explode(",", $sort_columns_str);
    $sort_columns_parsed = array();
    foreach ($sort_columns as $sort_column)
    {
        $direction = XSM_SORT_DIRECTION_ASC;
        $sort_column_name = $sort_column;
        if (xu_substr($sort_column, 0, 1) == "-")
        {
            $sort_column_name = xu_substr($sort_column, 1);
            $direction = XSM_SORT_DIRECTION_DESC;
        }
        // filter name, for safety
        $sort_column_name = preg_replace("/[^a-z_]/", "", $sort_column_name);
        if (xu_empty($sort_column_name))
        {
            // skip invalid columns
            continue;
        }
        $sort_columns_parsed[] = array(
            "name" => $sort_column_name,
            "direction" => $direction,
        );
    }
    return $sort_columns_parsed;
}

/**
 * Make JS init string for columns sorting
 */
function xsm_make_sort_columns_init($sort_columns)
{
    $sort_columns_init = array();
    foreach ($sort_columns as $sort_column_info)
    {
        $sort_column = $sort_column_info["name"];
        $direction = ($sort_column_info["direction"] == XSM_SORT_DIRECTION_DESC) ? "-" : "";
        $sort_columns_init[] = "\"$direction$sort_column\"";
    }
    return implode(", ", $sort_columns_init);
}

/**
 * Returns a HTML for insertion as table column header contents
 * @return formatted link html
 */
function xsm_sorted_column_header($id, $inner_html, $sorted_columns)
{
    $sort_icon = "&#x21e3;";  // default sorting is ASC
    $column_class = "";

    $my_column = array();
    foreach ($sorted_columns as $sort_column)
    {
        if ($id == $sort_column["name"])
        {
            $my_column = $sort_column;
            break;
        }
    }
    if (count($my_column))
    {
        $column_class = "sort_active";
        if ($my_column["direction"] == XSM_SORT_DIRECTION_ASC)
        {
            $sort_icon = "&#x21a1;";
        }
        elseif ($my_column["direction"] == XSM_SORT_DIRECTION_DESC)
        {
            $sort_icon = "&#x219f;";
        }
    }

    $inner_html = "$sort_icon&nbsp;$inner_html";
    return "<span id=\"sort_by_$id\" class=\"sort_by_inner $column_class\">$inner_html</span>";
}

/**
 * Устанавливает заголовок документу через JS
 */
function xsm_set_title($title)
{
    global $meta_site_name;
    ?>
    <span id="document_title-span" style="display: none;"><?php echo htmlspecialchars($title)
        ?> :: XSM :: <?php echo $meta_site_name; ?></span>
    <script>
    $(function(){
        document.title = $("#document_title-span").text();
    });
    </script><?php
}
