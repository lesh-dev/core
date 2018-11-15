<?php

function xsm_find_person_by_email($email)
{
    if (xu_empty($email)) {
        return null;
    }

    $db = xdb_get();
    $query = "SELECT * FROM person where email = '$email'";
    $person_sel = xdb_query($db, $query);
    while ($person = xdb_fetch($person_sel)) {
        return $person;
    }
    return null;
}
