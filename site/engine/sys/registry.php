<?php
    include_once("$engine_dir/sys/tag.php");

    /**
     * A-la registry API (for settings, etc)
     **/

    function xcms_get_registry_path()
    {
        global $content_dir;
        return "${content_dir}cms/registry.conf";
    }

    function xcms_get_registry()
    {
        return xcms_get_list(xcms_get_registry_path());
    }
