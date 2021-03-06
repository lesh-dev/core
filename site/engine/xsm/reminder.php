<?php
// Send notifications on NEW anketas

require_once("${xengine_dir}sys/template.php");
require_once("${engine_dir}cms/ank/fio.php");

function xsm_ank_reminder()
{
    $db = xdb_get();
    $time = time() - 1 * 24 * 3600; // one day
    $max_old = xcms_datetime($time);
    $query =
        "SELECT * FROM person WHERE
        (anketa_status = 'new') AND
        (person_created < '$max_old')
        ORDER BY person_created";

    $ank_reminder_table = "<ul>";
    $person_sel = xdb_query($db, $query);
    $empty_list = true;
    while ($person = xdb_fetch($person_sel)) {
        $empty_list = false;
        $full_name = xsm_fio_enc($person);
        $person_id = $person["person_id"];
        $ank_reminder_table .=
            '<li><a'.
            xsm_ext_href('view-person', array('person_id' => $person_id)).'>'.
            $full_name."</a></li>\n";
    }
    if ($empty_list) {
        return;
    }

    $ank_reminder_table .= "</ul>\n";
    $body_html = xcms_get_html_template("anketa_reminder");
    $body_html = str_replace('@@ANKETA-REMINDER@', $ank_reminder_table, $body_html);
    xcms_deliver_mail_int("reg-managers", array("dichlofos-mv@yandex.ru"), $body_html, "По состоянию на ".xcms_date()." есть необработанные анкеты");
}

?>