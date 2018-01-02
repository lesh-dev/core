<?php
global $engine_dir;
require_once("${engine_dir}cms/ank/field-desc.php");
require_once("${engine_dir}cms/ank/course.php");
require_once("${engine_dir}cms/ank/format.php");
require_once("${engine_dir}xsm/middleware.php");

require_once(translate("<! cms/ank/db-actions !>"));

$school_id = xsm_get_school_by_title($_0);
$db = xdb_get();
xsm_print_courses_selected_school($db, $school_id, "all", true);
?>