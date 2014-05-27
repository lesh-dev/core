<?php
/**
  * Получение person_school_id по person_id и school_id
  * @return person_school_id (или NULL)
  **/
function xsm_get_person_school_id($db, $school_id, $person_id)
{
    $ps_sel = $db->query(
        "SELECT
        ps.person_school_id
        FROM person_school ps WHERE
        (ps.member_person_id = $person_id) AND
        (ps.school_id = $school_id)"
    );

    if (!($ps_data = $ps_sel->fetchArray(SQLITE3_ASSOC)))
        return NULL;

    return $ps_data['person_school_id'];
}

/**
  * Специфическая функция: возврат происходит совсем в другую таблицу, нежели редактируемая сущность
  * TODO: Сделать более генерический update, чтобы можно было гибко обрабатывать и такие случаи тоже
  **/
function xsm_update_person_school($title, $fields)
{
    $db = xdb_get();
    $person_id = xcms_get_key_or($_POST, 'member_person_id', -1);
    $school_id = xcms_get_key_or($_POST, 'school_id', -1);
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
        $res = xdb_insert_or_update($table_name, array($key_name=>$id), $_POST, $fields);
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
    $redir = "view-person".xcms_url(array('person_id'=>$person_id, 'school_id'=>$school_id));
    ?>
    <a href="<?php echo $redir; ?>">Вернуться к просмотру участника</a></p><?php
}

// Специфическая функция для данной таблицы
function xsm_person_school_edit_operations($table_name, $id, $ret_title, $school_id, $member_person_id, $place)
{
    $is_new = ($id == XDB_NEW);
    $redir = "view-person".xcms_url(array('school_id'=>$school_id, 'person_id'=>$member_person_id));
    xsm_edit_ops($table_name, $is_new, $redir, $place, $ret_title, "Отчислить со школы");
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
    $redir = "$table_name".xcms_url(array($key_name=>$id));
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
    $redir = "view-person".xcms_url(array('person_id'=>$person_id, 'school_id'=>$school_id));
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
?>