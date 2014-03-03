<?php
// Anketa processor

function xsm_find_person_origin($db, $new_person)
{
    $last_name_esc = $db->escapeString(xcms_get_key_or($new_person, "last_name"));
    $first_name_esc = $db->escapeString(xcms_get_key_or($new_person, "first_name"));
    $patronymic_esc = $db->escapeString(xcms_get_key_or($new_person, "patronymic"));

    $id_fields = array(
        "birth_date",
        "email",
        "social_profile",
        "skype",
        "cellular",
        "phone");

    $query =
        "SELECT * FROM person WHERE
        (last_name = '$last_name_esc') AND
        (first_name = '$first_name_esc') AND
        (patronymic = '$patronymic_esc')
        ORDER BY person_created";

    $person_sel = $db->query($query);
    $matched_person_id = -1;
    $matched_person = false;
    while ($person = $person_sel->fetchArray(SQLITE3_ASSOC))
    {
        if ($person["anketa_status"] == "duplicate")
            continue;

        foreach ($id_fields as $id_key)
        {
            $value = xcms_get_key_or($new_person, $id_key);
            if (xu_not_empty($value) && $value == $person[$id_key])
            {
                // okay, match definitely found!
                $matched_person_id = $person['person_id'];
                $matched_person = $person;
                return $matched_person;
            }
        }
        // TODO: collect suspicious matches here
    }
    return false;
}


// TODO: test suite
function xsm_merge_persons($person_dst, $person_src)
{
    $person_fields = xsm_get_person_fields();
    $merge_state = "";

    foreach ($person_src as $key => $value)
    {
        // skip all unwanted fields
        if (!array_key_exists($key, $person_fields))
            continue;

        if (!array_key_exists($key, $person_dst))
        {
            // easy merge
            $person_dst[$key] = $value;
            continue;
        }

        // well, key exists

        // handle empty destination keys
        $old_val = $person_dst[$key];
        if (xu_len($old_val) == 0)
        {
            // easy merge
            $person_dst[$key] = $value;
            continue;
        }

        // keys are equal
        if ($person_dst[$key] == $value)
            continue;

        // old non-empty value is a prefix of new one
        if (xu_substr($value, 0, xu_len($old_val)) == $old_val)
        {
            $merge_state .= "[$key]: '$old_val' -> '$value'\n";
            $person_dst[$key] = $value;
            continue;
        }

        // most generic case: append
        $merge_state .= "[$key]: '$old_val' ++ '$value'\n";
        $person_dst[$key] .= "; $value";
    }

    return $person_dst;
}

function xsm_compose_anketa_table($person)
{
    $person_fields = xsm_get_person_fields();
    $html_content = ""; // @@TABLE-CONTENT@
    $row_template = xcms_get_html_template("anketa_mail_one_row");
    foreach ($person as $key=>$value)
    {
        $key_title = $key;
        if (array_key_exists($key, $person_fields))
            $key_title = $person_fields[$key];
        if ($key == "submit-anketa")
            continue;
        $cur_row = $row_template;
        $cur_row = str_replace("@@ANK-KEY@", $key_title, $cur_row);
        $cur_row = str_replace("@@ANK-VALUE@", htmlspecialchars($value), $cur_row);
        $html_content .=  $cur_row;
    }
    return $html_content;
}

function xsm_compose_anketa_mail_msg($person, $html_content)
{
    $person_id = $person["person_id"];

    $mail_msg = xcms_get_html_template("anketa_mail");
    $hr_timestamp = xcms_datetime();

    $full_name_enc = xsm_fio_enc($person);
    $table_title = 'Анкета: <a'.
        xsm_ext_href('view-person', array('person_id'=>$person_id)).'>'.
        $full_name_enc."</a> ($hr_timestamp)";
    $mail_msg = str_replace("@@TABLE-CONTENT@", $html_content, $mail_msg);
    $mail_msg = str_replace("@@TABLE-TITLE@", $table_title, $mail_msg);
    $mail_msg = str_replace("@@HOST@", xcms_hostname(), $mail_msg);

    return $mail_msg;
}

function xsm_compose_anketa_reply_link($first_name, $email)
{
    // prepare reply_link
    $reply_link = xcms_get_html_template("anketa_reply_link");
    $reply_body = xcms_get_html_template("anketa_reply_body");
    $reply_body = str_replace("@@NAME@", $first_name, $reply_body);
    // TODO hardcoded subject
    $reply_link = str_replace("@@REPLY-SUBJECT@", rawurlencode("ФизЛЭШ: Анкета принята"), $reply_link);
    $reply_link = str_replace("@@REPLY-BODY@", str_replace("\n", "<br />", $reply_body), $reply_link);
    $reply_link = str_replace("@@REPLY-BODY-ENC@", rawurlencode($reply_body), $reply_link);
    $reply_link = str_replace("@@REPLY-TO@", $email, $reply_link);
}



?>