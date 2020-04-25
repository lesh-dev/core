<!DOCTYPE html>
<html>
<body><?php

$engine_dir = "engine/";
$xengine_dir = "xengine/";
$full_xengine_dir = "${_SERVER["DOCUMENT_ROOT"]}/xengine/";

session_start();

require_once("${xengine_dir}sys/db.php");
require_once("${engine_dir}cms/ank/format.php");
require_once("${engine_dir}cms/ank/person.php");

$SETTINGS["content_dir"] = "content/";

$SETTINGS[XDB_DB_TYPE] = XDB_DB_TYPE_PG;
$SETTINGS[XDB_DB_NAME] = "host=localhost user=lesh password=fizlesh dbname=lesh";

xsm_increase_class_numbers();

?></body></html>