<?php

function xsm_get_vk_uid($social_profile)
{
    $match = array();
    // match id vk
    preg_match("/.*vk.com\/id([0-9]+)/", $social_profile, $match);
    if (count($match))
        return $match[1];

    // match id vkontakte
    preg_match("/.*vkontakte.ru\/id([0-9]+)/", $social_profile, $match);
    if (count($match))
        return $match[1];

    // match alias vk
    preg_match("/.*vk.com\/([A-Za-z._0-9]+)/", $social_profile, $match);
    if (count($match))
        return $match[1];

    // match alias vkontakte
    preg_match("/.*vkontakte.ru\/([A-Za-z._0-9]+)/", $social_profile, $match);
    if (count($match))
        return $match[1];

    return false;
}


function xsm_get_avatar($social_profile)
{
    // TODO: extract first profile (e.g. by spaces)
    // set default av
    global $full_engine_pub;
    $av = "${full_engine_pub}img/stalin50.jpg";
    $vk_uid = xsm_get_vk_uid($social_profile);
    if ($vk_uid === false)
        return $av;

    $cache_dir = ".prec/avatar-cache";
    @mkdir($cache_dir, 0777);

    $json_fn = "$cache_dir/vk-json-$vk_uid";
    $update_cache = false;
    if (file_exists($json_fn))
    {
        $fmt = @filemtime($json_fn);
        if ($fmt && time() - $fmt > 3600 * 24 * 14)
            $update_cache = true;
    }
    else
        $update_cache = true;

    $wget_cmd = "wget 'https://api.vk.com/method/getProfiles?uids=$vk_uid&fields=photo&v=1' -O $json_fn";
    if ($update_cache && (0 != system($wget_cmd)))
        return $av;

    $json_text = file_get_contents($json_fn);
    $json = @json_decode($json_text, true);
    if (!is_array($json))
        return $av;
    if (!array_key_exists('response', $json))
        return $av;
    $response = $json['response'];
    // VK returns empty array on invalid uid
    if (count($response) > 0)
    {
        $av = $response[0]['photo'];
    }
    return $av;
}


function xsm_increase_class_numbers()
{
    xcms_auth_wall_admin();

    // lock database
    $db = xdb_get_write();

    $query =
        "SELECT
            p.person_id,
            p.current_class
        FROM person p
        WHERE
            (
                (anketa_status = 'new') OR
                (anketa_status = 'progress') OR
                (anketa_status = 'less') OR
                (anketa_status = 'processed') OR
                (anketa_status = 'discuss') OR
                (anketa_status = 'nextyear') OR
                (anketa_status = 'cont')
            )
            AND LENGTH(is_student) > 0
            AND p.department_id = 1
        ";

    xdb_debug_area($query, XDB_DEBUG_AREA_DISABLED);
    $person_sel = $db->query($query);

    $selected_persons = array();

    while ($person = $person_sel->fetchArray(SQLITE3_ASSOC))
    {
        $person_id = $person["person_id"];
        $person_link = xsm_person_view_link($person_id, XSM_SCHOOL_ANK_ID, "", "/xsm/");
        $current_class = $person["current_class"];
        $current_class_int = xsm_class_num($current_class);
        if (preg_match("/[0-9]+/", $current_class_int))
        {
            $current_class_int = (integer)$current_class_int;
            if ($current_class_int < 11)
            {
                $current_class_int += 1;
            }
            else
            {
                $current_class_int = "n/a";
            }
            $selected_persons[$person_id] = array(
                "current_class" => $current_class_int,
                "old_class" => $current_class,
            );
            echo "Поднимаем класс у $person_link с [$current_class] до [$current_class_int]<br/>";
        }
        else
        {
            echo "<span class=\"error\">Невозможно поднять класс у $person_link, что-то нечитаемое: [$current_class]<br/>";
        }
    }

    $operator = xcms_user()->login();
    $current_timestamp = xcms_datetime();
    $person_fields = xsm_get_fields("person");
    $person_comment_fields = xsm_get_fields("person_comment");
    foreach ($selected_persons as $person_id => $updated_fields)
    {
        xdb_update(
            "person",
            array("person_id" => $person_id),
            $updated_fields,
            $person_fields,
            XDB_OVERRIDE_TS,
            $db
        );

        $old_class = $updated_fields["old_class"];
        $current_class = $updated_fields["current_class"];
        $person_comment = array(
            "owner_login" => $operator,
            "comment_text" => "Класс изменён с [$old_class] на [$current_class] пользователем $operator ($current_timestamp).",
            "blamed_person_id" => $person_id,
        );
        $res = xdb_insert_or_update('person_comment', array('person_comment_id' => XDB_NEW), $person_comment, $person_comment_fields, $db);
        if (!$res)
        {
            die("Не удалось добавить комментарий, обратитесь на dev@fizlesh.ru. ");
            return;
        }
    }
    echo "<a href=\"/xsm/list-person-locator\">Вернуться к списку</a>\n";
}
