<?php
require_once("${engine_dir}cms/ank/course_teacher.php");

/**
  * Печаталка таблицы курсов (общая для списка курсов на школе и одного препода)
  **/
function xsm_print_courses_selected_school(
    $db, $school_id,
    $course_teacher_id = "all",
    $simple_view = false,
    $show_desc = false)
{
    $pers = ($course_teacher_id != "all");
    global $XSM_BOOTSTRAP;

    $query =
    "SELECT *
    FROM course c
    WHERE (c.school_id = $school_id)
    ORDER BY course_title";

    $person_list_link = xsm_person_list_link($school_id);
    $ht = $pers ? "h2" : "h1";
    $table_title = "<$ht>Курсы на $person_list_link</$ht>";

    $course_sel = $db->query($query);
    $course_aux_param = $pers
        ? xcms_url(array(
            'course_teacher_id'=>$course_teacher_id,
            'school_id'=>$school_id))
        : xcms_url(array(
            'school_id'=>$school_id));

    if (!$simple_view)
    {
        echo $table_title;
        xsm_view_operations('course', 'курс', $course_aux_param); ?>
    <table class="ankList table table-bordered table-hover table-condensed">
        <colgroup>
        <?php
        if ($XSM_BOOTSTRAP) {?>
            <col width="20%" />
            <?php if (!$pers) {?>
            <col width="20%" /><?php
            } ?>
            <col width="1%" />
            <col width="1%" />
            <col width="12%" />
            <col width="5%" />
            <col width="12%" />
            <?php if ($show_desc) {?>
            <col width="20%" /><?php
            }
        } else {?>
            <col width="20%" />
            <?php if (!$pers) {?>
            <col width="20%" /><?php
            } ?>
            <col width="2%" />
            <col width="8%" />
            <col width="8%" />
            <col width="3%" />
            <col width="3%" />
            <?php if ($show_desc) {?>
            <col width="20%" /><?php
            }
        }?>
        </colgroup>
        <thead>
            <th class="ankList">Курс</th>
            <?php if (!$pers) {?>
            <th class="ankList">Препод</th><?php
            } ?>
            <th class="ankList">Цикл</th>
            <th class="ankList">Тип</th>
            <th class="ankList">Тематика</th>
            <th class="ankList">Класс</th>
            <th class="ankList">Успехи</th>
            <?php if ($show_desc) {?>
            <th class="ankList">Описание, комментарий</th><?php
            }
        ?>
        </thead>
    <?php
    } else {?><ul><?php }

    $course_count = 0;
    while ($course = $course_sel->fetchArray(SQLITE3_ASSOC))
    {
        ++$course_count;
        $course_id = xcms_get_key_or_enc($course, "course_id");
        $course_title = xcms_get_key_or_enc($course, "course_title", "<без названия>");
        $target_class = xcms_get_key_or_enc($course, "target_class");
        $course_cycle = xcms_get_key_or_enc($course, "course_cycle");
        $hr_course_type = xsm_make_enum($course, "course_type", $course_count);
        $hr_course_area = xsm_make_enum($course, "course_area", $course_count);

        $comments = array();
        $course_desc = xcms_html_wrap_by_crlf(xsm_highlight_links($course['course_desc']));
        if (xu_not_empty($course_desc))
            $comments[] = $course_desc;

        $course_comment = xcms_html_wrap_by_crlf(xsm_highlight_links($course['course_comment']));
        if (xu_not_empty($course_count))
            $comments[] = $course_comment;

        $course_desc_comment = implode("<br />", $comments);

        $teachers_ht = xsm_get_course_teachers($db, $course_id, $school_id, $course_teacher_id);
        if ($teachers_ht === false) // filter not passed
            continue;

        $simple_teachers_ht = "";
        if ($simple_view)
        {
            $simple_ct = xsm_get_course_teachers_list($db, $course_id, $school_id);
            foreach ($simple_ct as $ct_id => $teacher_data)
            {
                if ($teacher_data['course_teacher_id'] == 13) // Преподаватель Другого Отделения
                    continue;
                $teacher_fi = xsm_fi_enc($teacher_data);
                if (xu_not_empty($simple_teachers_ht))
                    $simple_teachers_ht .= ", ";
                $simple_teachers_ht .= $teacher_fi;
            }
        }

        // ахтунг, тут будет 3*N SELECT-ов
        // до кучи посчитаем количество сдавших
        $exam_passed_sel = $db->query(
            "SELECT
            COUNT(*) AS pass_count from exam
            WHERE
            (course_id = '$course_id') AND
            (exam_status = 'passed')"
        );
        $exam_pass_count = 0;
        if ($exam_pass_data = $exam_passed_sel->fetchArray(SQLITE3_ASSOC))
            $exam_pass_count = $exam_pass_data['pass_count'];
        $exam_total_sel = $db->query(
            "SELECT
            COUNT(*) AS total_count from exam
            WHERE
            (course_id = '$course_id')"
        );
        $exam_total_count = 0;
        if ($exam_total_data = $exam_total_sel->fetchArray(SQLITE3_ASSOC))
            $exam_total_count = $exam_total_data['total_count'];
        $course_url = "view-course".xcms_url(array('course_id'=>$course_id));

        if (!$simple_view)
        {?>
        <tr>
            <td class="ankList"><a href="<?php echo $course_url; ?>"><?php
                echo $course_title; ?></a></td>
            <?php if (!$pers) {?>
            <td class="ankList"><?php echo $teachers_ht; ?></td>
            <?php } ?>
            <td class="ankList c"><?php echo $course_cycle; ?></td>
            <td class="ankList"><?php echo $hr_course_type; ?></td>
            <td class="ankList"><?php echo $hr_course_area; ?></td>
            <td class="ankList"><?php echo $target_class; ?></td>
            <td class="ankList"><a href="<?php echo $course_url; ?>"><?php
                echo "<b>$exam_pass_count</b>&nbsp;из&nbsp;<b>$exam_total_count</b>"; ?></a></td>

            <?php if ($show_desc) {?>
            <td class="ankList"><?php echo $course_desc_comment; ?></td><?php
            }?>

        </tr><?php
        } else
        {
            // пока что не показывать курсы
            // преподов других отделений. Как только у нас будет разделение по отделениям,
            // мы сразу это запилим правильно (а это будет уже довольно скоро)
            if (strlen($simple_teachers_ht))
            {?>
                <li><?php echo $course_title; ?>&nbsp;&ndash;&nbsp;<i><?php
                    echo $simple_teachers_ht; ?></i></li><?php
            }
        }
    }
    if (!$simple_view)
    {?></table><?php }
    else {?></ul><?php }
}

?>