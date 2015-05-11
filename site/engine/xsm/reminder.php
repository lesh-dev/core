<?php
// Send notifications on NEW anketas

function xsm_ank_reminder()
{
    $time = time() - 1 * 24 * 3600; // one day
    $max_old = xcms_datetime($time);
    $query =
        "SELECT * FROM person WHERE
        (anketa_status = 'new') AND
        (person_created < '$max_old')
        ORDER BY person_created";

    $ank_reminder_table = "<ul>";
    $person_sel = $db->query($query);
    while ($person = $person_sel->fetchArray(SQLITE3_ASSOC))
    {
        $full_name = xsm_fio_enc($person);
        $person_id = $person["person_id"];
        $ank_reminder_table .=
            '<li><a'.
            xsm_ext_href('view-person', array('person_id'=>$person_id)).'>'.
            $full_name."</a></li>\n";
    }
    $ank_reminder_table .= "</ul>\n";
    $body_html = xcms_get_html_template("anketa_reminder");
    $body_html = str_replace('@@ANKETA-REMINDER@', $ank_reminder_table, $body_html);
    xcms_send_notification("reg", "dichlofos-mv@yandex.ru", $body_html);
}

?>