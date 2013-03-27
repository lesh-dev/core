<?php
    $LIST["installed"] = "ok";
    $LIST["maxNews"] = 10;
    $INFO["installed"] = "ok";
    $INFO["maxNews"] = 10;

    xcms_save_list(xcms_get_info_file_name(), $INFO);
    $template_name = "{$SETTINGS["datadir"]}cms/pages/$pageid/template";
    $f = fopen($template_name, "w");
    if ($f)
    {
        fputs($f,
            '<div class="newstitle">@@DATE@. Заголовок новости</div>'."\n".
            '<p class="text">Текст новости</p>'."\n".
            '<div class="signature">@@AUTHOR@</div>');
        fclose($f);
    }
    else
    {
        xcms_log(0, "[NEWS INSTALLER]: Cannot find template file '$template_name'");
    }
?>