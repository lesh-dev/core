<!DOCTYPE html>
<html>
<body><?php

$engine_dir = "engine/";
$xengine_dir = "xengine/";

$SETTINGS["content_dir"] = "content/";
$SETTINGS['xsm_db_name'] = 'content/ank/fizlesh.sqlite3';

session_start();

require_once("${xengine_dir}sys/db.php");
require_once("${engine_dir}cms/ank/format.php");
require_once("${engine_dir}cms/ank/person.php");

xsm_increase_class_numbers();

?></body></html>