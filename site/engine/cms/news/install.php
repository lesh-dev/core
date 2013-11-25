<?php
    $LIST["installed"] = "ok";
    $LIST["maxNews"] = 10;
    $INFO["installed"] = "ok";
    $INFO["maxNews"] = 10;

    xcms_save_list(xcms_get_info_file_name(), $INFO);
    $template_name = "{$SETTINGS["content_dir"]}cms/pages/$pageid/template";
    if (!xcms_write(
        $template_name,
        '<div class="newstitle">@@DATE@. Заголовок новости</div>'.EXP_LF.
        '<p class="text">Текст новости</p>'.EXP_LF.
        '<div class="signature">@@AUTHOR@</div>')
    {
        xcms_log(0, "[NEWS INSTALLER]: Cannot write template file '$template_name'");
    }
?>