<?php
// Person merger

function xsm_find_match($db, $new_person)
{
    // TODO: escape here
    $last_name_esc = $last_name;
    $first_name_esc = $first_name;
    // TODO: check non-void FIO
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
        if (xu_not_empty($birth_date) && $birth_date == $person['birth_date'])
        {
            // okay, match definitely found!
            $matched_person_id = $person['person_id'];
            $matched_person = $person;
            break;
        }
    }
    return $matched_person;
}


function xsm_merge_persons($person_dst, $person_src)
{
    foreach ($person_src as $key => $value)
    {
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
}



?>