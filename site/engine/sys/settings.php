<?php
    require_once("settings.php");
    global $SETTINGS;
    $SETTINGS["defaultpage"] = "index";
    $SETTINGS["nopagecode"] = "error.404";
    $SETTINGS["openbracket"] = "<# ";
    $SETTINGS["closebracket"] = "#>";
    $SETTINGS["engine_dir"] = $engine_dir;
    $SETTINGS["engine_pub"] = $engine_pub;
    $SETTINGS["documentsdir"] = $design_dir;
    $SETTINGS["design_dir"] = $design_dir;
    $SETTINGS["content_dir"] = $content_dir;
    $SETTINGS["precdir"] = ".prec/";
    $SETTINGS["code_begin"] = '<?php unset($argv);unset($param);';
    $SETTINGS["code_end"] = '?>';
    $SETTINGS["mailer_enabled"] = $mailer_enabled;
    // auth session lifetime in seconds
    $SETTINGS["session_time"] = 7*24*3600;
    // redirect delay in seconds (for autotesting needs)
    $SETTINGS["zero_redirect_delay"] = "0";
    // content versioning roundup
    $SETTINGS["content_time_roundup"] = 100;

    // set up some common-used things
    global $full_content_dir;
    global $full_design_dir;
    global $full_engine_pub;

    global $meta_site_url;
    global $meta_site_url_secure;
    $meta_site_url_secure = str_replace("http:", "https:", $meta_site_url);

    $full_content_dir = "/$web_prefix${content_dir}";
    $full_design_dir = "/$web_prefix${design_dir}";
    $full_engine_pub = "/${web_prefix}{$SETTINGS["engine_pub"]}";
?>
