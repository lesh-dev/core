<?php
// Anketa processor

function xsm_extract_phone_digits($phones_str)
{
    $phones = xsm_format_phones($phones_str);
    $phones_digits = array();
    foreach ($phones as $phone)
    {
        $digits = xcms_get_key_or($phone, "digits");
        if (xu_empty($digits))
            continue;
        $phones_digits[] = $digits;
    }
    return $phones_digits;
}

function xsm_extract_person_phone_digits($person)
{
    $phone = xsm_extract_phone_digits(xcms_get_key_or($person, "phone"));
    $cellular = xsm_extract_phone_digits(xcms_get_key_or($person, "cellular"));
    return array_merge($phone, $cellular);
}

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
        "phone",
    );

    $query =
        "SELECT * FROM person WHERE
        (last_name = '$last_name_esc') AND
        (first_name = '$first_name_esc') AND
        (patronymic = '$patronymic_esc')
        ORDER BY person_created";

    $person_sel = $db->query($query);
    $matched_person_id = XDB_INVALID_ID;
    $matched_person = false;

    $new_phones = xsm_extract_person_phone_digits($new_person);

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
        // #885
        $old_phones = xsm_extract_person_phone_digits($person);
        if (count(array_intersect($new_phones, $old_phones)))
        {
            $matched_person_id = $person['person_id'];
            $matched_person = $person;
            return $matched_person;
        }
    }
    return false;
}

/**
  * Fields that cannot be merged via text addition
  **/
function xsm_non_mergeable_person_key($key)
{
    return (
        $key == "anketa_status" ||
        $key == "department_id" ||
        $key == "is_student" ||
        $key == "is_teacher" ||
        false
    );
}

function xsm_ignored_person_key($key)
{
    return (
        $key == "user_agent" ||
        false
    );
}

/**
  * Performs persons merge
  * @return: array of keys:
  *   "person": merged person kv-array
  *   "state": merge state
  **/
function xsm_merge_persons($person_dst, $person_src)
{
    $fields_desc = xsm_get_fields("person");
    $merge_state = "";

    foreach ($person_src as $key => $value)
    {
        // skip all unwanted fields
        if (!array_key_exists($key, $fields_desc))
            continue;
        if (xsm_ignored_person_key($key))
            continue;

        $value = trim($value);
        $desc = $fields_desc[$key];
        $key_title = $desc["name"];

        if (xsm_non_mergeable_person_key($key))
        {
            $merge_state .= "$key_title: set '$value'\n";
            $person_dst[$key] = $value;
            continue;
        }

        if (!array_key_exists($key, $person_dst))
        {
            // easy merge
            $person_dst[$key] = $value;
            continue;
        }

        // well, key exists

        // handle empty destination keys
        $old_val = trim($person_dst[$key]);
        if (xu_len($old_val) == 0)
        {
            // easy merge
            $person_dst[$key] = $value;
            continue;
        }

        if (xu_len($value) == 0)
        {
            // nothing to merge
            continue;
        }

        // keys are equal
        if ($old_val == $value)
            continue;

        // old non-empty value is a prefix of new one
        if (xu_substr($value, 0, xu_len($old_val)) == $old_val)
        {

            $merge_state .= "$key_title: '$old_val' -> '$value'\n";
            $person_dst[$key] = $value;
            continue;
        }

        // most generic case: append
        $merge_state .= "$key_title: '$old_val' += '$value'\n";
        $person_dst[$key] .= "; $value";
    }

    return array(
        "person"=>$person_dst,
        "state"=>$merge_state,
    );
}

function xsm_compose_anketa_table($person)
{
    $fields_desc = xsm_get_fields("person");
    $html_content = ""; // @@TABLE-CONTENT@
    $row_template = xcms_get_html_template("anketa_mail_one_row");
    foreach ($person as $key=>$value)
    {
        $key_title = $key;
        if (array_key_exists($key, $fields_desc))
            $key_title = $fields_desc[$key]["name"];
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

    return $reply_link;
}

function xsm_ank_proc_unit_test()
{
    xut_begin("ank-proc");

    // test #885
    $new_person = array(
        "person_id"=>1,
        "phone"=>"84951659121",
        "cellular"=>"+79161686186",
    );
    $old_person = array(
        "person_id"=>1,
        "cellular"=>"+74951659121",
        "phone"=>"89161686186, 89146661666",
    );
    $new_phones = xsm_extract_person_phone_digits($new_person);
    $old_phones = xsm_extract_person_phone_digits($old_person);
    $count = count(array_intersect($new_phones, $old_phones));
    xut_equal($count, 2, "Nonzero common phone count");

    $old_person = array(
        "person_id"=>1,
        "cellular"=>"",
        "phone"=>"100",
    );
    $old_phones = xsm_extract_person_phone_digits($old_person);
    $count = count(array_intersect($new_phones, $old_phones));
    xut_equal($count, 0, "Zero common phone count");

    xut_end();
}

?>