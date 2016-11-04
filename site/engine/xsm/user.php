<?php

function xsm_find_person_by_email($email)
{
    if (xu_empty($email))
        return null;

    $db = xdb_get();
    $query = "SELECT * FROM person where email = '$email'";
    $person_sel = $db->query($query);
    while ($person = $person_sel->fetchArray(SQLITE3_ASSOC))
    {
        return $person;
    }
    return null;
}
