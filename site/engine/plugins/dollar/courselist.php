<?php
include(translate("<! cms/ank/field-desc !>"));
include(translate("<! cms/ank/db-actions !>"));
include(translate("<! cms/ank/middleware !>"));
include(translate("<! cms/ank/format !>"));

$school_id = xsm_get_school_by_title($_0);
$db = xdb_get();
xsm_print_course_selected_school($db, $school_id, "all", true);
?>