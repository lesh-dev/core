<?php
/**
  * Получение person_school_id по person_id и school_id
  * @return person_school_id (или NULL)
  **/
function xsm_get_person_school_id($db, $school_id, $person_id)
{
    $ps_sel = xdb_query(
        $db,
        "SELECT
        ps.person_school_id
        FROM person_school ps WHERE
        (ps.member_person_id = '$person_id') AND
        (ps.school_id = '$school_id')"
    );

    if (!($ps_data = xdb_fetch($ps_sel))) {
        return null;
    }

    return $ps_data['person_school_id'];
}

/**
  * Специфическая функция: возврат происходит совсем в другую таблицу, нежели редактируемая сущность
  * TODO: Сделать более генерический update, чтобы можно было гибко обрабатывать и такие случаи тоже
  **/
function xsm_update_person_school($title, $fields_desc)
{
    $db = xdb_get();
    $person_id = xcms_get_key_or($_POST, 'member_person_id', XDB_INVALID_ID);
    $school_id = xcms_get_key_or($_POST, 'school_id', XDB_INVALID_ID);
    $person_school_id = xsm_get_person_school_id($db, $school_id, $person_id);
    $table_name = "person_school";
    $key_name = "${table_name}_id";
    $id = xcms_get_key_or($_POST, $key_name, 'invalid'); // invalid key
    if ($id == XDB_NEW && $person_school_id !== NULL)
    {?>
        <p>Этот участник уже зачислен на данную школу.<?php
    }
    else
    {
        $res = xdb_insert_or_update($table_name, array($key_name => $id), $_POST, $fields_desc);
        if ($res)
        {
            $id = $res;
            ?>
            <p><?php echo $title; ?> успешно сохранён.<?php
        }
        else
        {?>
            <p>Не удалось добавить <?php echo $title; ?>.<?php
        }
    }
    $redir = "view-person".xcms_url(array('person_id' => $person_id, 'school_id' => $school_id));
    ?>
    <a href="<?php echo $redir; ?>">Вернуться к просмотру участника</a></p><?php
}

function xsm_add_person_to_school($school_id, $person_id)
{
    if ($school_id == XDB_INVALID_ID)
    {
        die("XSM internal error, please report to dev@fizlesh.ru. ");
        return;
    }

    $db = xdb_get();
    $person_school_id = xsm_get_person_school_id($db, $school_id, $person_id);
    if ($person_school_id !== NULL || $school_id == XSM_SCHOOL_ANK_ID)
        return;

    $person_school = array(
        'school_id' => $school_id,
        'member_person_id' => $person_id,
        'is_teacher' => $_REQUEST['is_teacher'],
        'is_student' => $_REQUEST['is_student'],
        'member_department_id' => $_REQUEST['department_id'],
    );
    $ps_result = xdb_insert_or_update("person_school", array("person_school_id" => XDB_NEW),
        $person_school, xsm_get_fields("person_school"));

    $person = xdb_get_entity_by_id('person', $person_id);
    $fi = xsm_fi_enc($person);
    $person_list_link = xsm_person_list_link($school_id);
    if ($ps_result === false)
    {?>
        <p>Не удалось зачислить участника <?php echo $fi; ?>
        на школу <?php echo $person_list_link; ?></p><?php
    }
    else
    {?>
        <p>Участник <?php echo $fi; ?> успешно зачислен
        на школу <?php echo $person_list_link; ?></p><?php
    }
}

// Специфическая функция для данной таблицы
function xsm_person_school_edit_operations($table_name, $id, $ret_title, $school_id, $member_person_id)
{
    $is_new = ($id == XDB_NEW);
    $redir = "view-person".xcms_url(array('school_id' => $school_id, 'person_id' => $member_person_id));
    xsm_edit_ops($table_name, $is_new, $redir, $ret_title, "Отчислить со школы");
}

/* Ещё одна специфическая функция -- возврат на редактирование, а не на просмотр,
т.к. просмотра отдельно не существует) */
function xsm_warn_delete_person_school($table_name, $id = false)
{
    $key_name = "${table_name}_id";
    if ($id === false) // okay, take it from request
        $id = xcms_get_key_or($_POST, $key_name, 'invalid'); // invalid key
    $person_school = xdb_get_entity_by_id($table_name, $id);
    $person_id = $person_school['member_person_id'];
    $school_id = $person_school['school_id'];
    $person = xdb_get_entity_by_id('person', $person_id);
    $school = xdb_get_entity_by_id('school', $school_id);
    $first_name = xcms_get_key_or($person, 'first_name');
    $last_name = xcms_get_key_or($person, 'last_name');
    $school_title = xcms_get_key_or($school, 'school_title');
    $redir = "$table_name".xcms_url(array($key_name => $id));
    xsm_warn_delete_ops($table_name, $key_name, $id, $redir, "участника",
        "<b>$first_name $last_name</b> со школы <b>$school_title</b>");
}

function xsm_delete_person_school($table_name, $title, $aux_param = '')
{
    $key_name = "${table_name}_id";
    $id = xcms_get_key_or($_POST, $key_name, 'invalid'); // invalid key
    $person_school = xdb_get_entity_by_id('person_school', $id);
    $person_id = $person_school['member_person_id'];
    $school_id = $person_school['school_id'];
    $redir = "view-person".xcms_url(array('person_id' => $person_id, 'school_id' => $school_id));
    $res = xdb_delete($table_name, $id);
    if ($res)
    {?>
        <p><?php echo $title; ?> [<?php echo $id; ?>] удалён успешно.<?php
    }
    else
    {?>
        <p>Не удалось удалить <?php echo $title; ?> [<?php echo $id; ?>] (возможно, есть связанные объекты).<?php
    }?>
    <a href="<?php echo $redir ?>">Вернуться к просмотру участника</a></p><?php
}

function xsm_output_school_participants_list($person_sel, $school_id)
{
    global $show_patronymic;

    $db = xdb_get();
    $school = xdb_get_entity_by_id('school', $school_id);
    $school_title = xcms_get_key_or_enc($school, 'school_title');
    $student_count = 0;
    $teacher_count = 0;
    ?>
    <table class="ankList table table-bordered table-hover table-condensed">
        <colgroup>
            <col width="1%">
            <col width="10%">
            <col width="5%">
            <col width="5%">
            <col width="5%">
            <col width="5%">
            <col width="25%">
            <col width="25%">
        </colgroup>
        <thead>
        <th class="ankList">#</th>
        <th class="ankList">Фамилия, имя</th>
        <th class="ankList">Зач.</th>
        <th class="ankList">Кур.</th>
        <th class="ankList">Кл.&nbsp;шк.&nbsp;/&nbsp;Кл.</th>
        <th class="ankList">ДР</th>
        <th class="ankList">Контакты</th>
        <th class="ankList">Комментарий</th>
        </thead>
        <?php
        while ($person = $person_sel->fetchArray(SQLITE3_ASSOC))
        {
            $person_id = htmlspecialchars($person["person_id"]);

            $fin = xsm_fin_enc($person);
            $fio = xsm_fio_enc($person);
            $display_name = $show_patronymic ? $fio : $fin;

            $p_current_class = xsm_class_num(xcms_get_key_or_enc($person, "p_current_class"));
            $ps_current_class = xsm_class_num(xcms_get_key_or_enc($person, "ps_current_class"));

            $birth_date = xcms_get_key_or_enc($person, "birth_date");
            $birth_date = str_replace(".07.", "<b>.07.</b>", $birth_date);
            $birth_date = str_replace(".08.", "<b>.08.</b>", $birth_date);

            $contacts = xsm_contacts_for_list($person);

            $is_teacher = $person["is_teacher"];
            $is_student = $person["is_student"];
            $curatorship = $person["curatorship"];
            $curator_group = $person["curator_group"];
            $courses_needed = $person["courses_needed"];

            $person_created = xsm_ymdhm($person["person_created"]);
            $person_modified = xsm_ymdhm($person["person_modified"]);

            $courses_passed = xdb_count($db, "SELECT
            COUNT(*) AS cnt
            FROM exam e, course c
            WHERE
            (e.student_person_id = $person_id) AND
            (c.school_id = $school_id) AND
            (e.course_id = c.course_id) AND
            (e.exam_status = 'passed')"
            );
            $course_ratio = ($courses_needed > 0) ? ($courses_passed / $courses_needed) : -1;

            $hr_course_progress = "$courses_passed&nbsp;/&nbsp;$courses_needed";
            if ($course_ratio < -0.5)
                $hr_course_progress = "&#8212;";

            $course_style = xsm_calc_course_style($course_ratio);

            $num = "";
            if (xcms_checkbox_enabled($is_student))
            {
                $student_count++;
                $num = $student_count;
            }
            elseif (xcms_checkbox_enabled($is_teacher))
            {
                $teacher_count++;
                $num = $teacher_count;
            }

            $person_school_url = "view-person".xcms_url(array(
                    'person_id' => $person_id,
                    'school_id' => $school_id));

            $person_school_comment = xcms_html_wrap_by_crlf(xsm_highlight_links($person['person_school_comment']));

            $row_class = (xcms_checkbox_enabled($is_teacher) ? "teacher" : "");
            $class_diff = ($ps_current_class != $p_current_class) ? "diff" : "";
            ?>
            <tr class="<?php echo $row_class; ?>">
                <td class="ankList"><?php echo $num; ?></td>
                <td class="ankList">
                    <a name="<?php echo "person$person_id"; ?>"></a>
                    <a href="<?php echo $person_school_url; ?>"
                        title="<?php echo $fio; ?>"><?php echo $display_name; ?></a></td>
                <td class="ankList"><span class="course-progress <?php echo $course_style; ?>"><?php
                        echo $hr_course_progress; ?></span></td>
                <td class="ankList"><?php echo $curator_group; ?></td>
                <td class="ankList"><span class="class-school-num <?php echo $class_diff; ?>"
                    title="Класс на <?php echo $school_title; ?>"><?php echo $ps_current_class;
                        ?></span>&nbsp;/&nbsp;<span
                        class="class-current-num"
                        title="Текущий класс"><?php echo $p_current_class; ?></span></td>
                <td class="ankList"><?php echo $birth_date; ?></td>
                <td class="ankList"><?php echo $contacts; ?></td>
                <td class="ankList"><?php echo $person_school_comment; ?></td>
            </tr>
            <?php
        }
        ?>
    </table>
    <?php
}
?>