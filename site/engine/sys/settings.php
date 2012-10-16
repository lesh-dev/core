<?php
    include("settings.php");
    $SETTINGS["defaultpage"] = "index";
    $SETTINGS["nopage"] = ".nopage";
    $SETTINGS["nopagecode"] = "error.404";
    $SETTINGS["openbracket"] = "<# ";
    $SETTINGS["closebracket"] = "#>";
    $SETTINGS["elementsdir"] = $engine_dir;
    $SETTINGS["documentsdir"] = $design_dir;
    $SETTINGS["design_dir"] = $design_dir;
    $SETTINGS["datadir"] = $content_dir;
    $SETTINGS["precdir"] = ".prec/";
    $SETTINGS["code_begin"] = '<?php unset($argv);unset($keys);unset($param);';
    $SETTINGS["code_end"] = '?>';
    $SETTINGS["mailer_enabled"] = $mailer_enabled;
    // auth session lifetime in seconds
    $SETTINGS["session_time"] = 7*24*3600;
    // redirect delay in seconds (for autotesting needs)
    $SETTINGS["zero_redirect_delay"] = "0";
?>
