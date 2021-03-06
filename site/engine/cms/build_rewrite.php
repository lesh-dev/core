<?php

/**
  * @return dict("error", "output").
  * error can be either `false` or error message.
  **/
function _xcms_build_rewrite()
{

    global $full_design_dir;
    global $content_dir;
    global $engine_dir;
    global $web_prefix;

    $error = false;
    $html_output = "";

    $rewrite_header_fn = "${engine_dir}cms/header.htaccess";
    if (!file_exists($rewrite_header_fn))
    {
        die("Cannot find rewrite template header, alias translation will not work.");
        xcms_log(XLOG_ERROR, "[XCMS:REWRITE] Cannot find rewrite template header");
    }
    $rewrite_text = file_get_contents($rewrite_header_fn);
    $rewrite_text = str_replace('@@DESIGN-DIR@', $full_design_dir, $rewrite_text);
    $rewrite_text = str_replace('@@WEB-PREFIX@', "/$web_prefix", $rewrite_text);
    $rewrite_text .= "\n";

    $custom_rewrite_fn = "${content_dir}cms/moved-pages";
    if (file_exists($custom_rewrite_fn))
    {
        $rewrite_text .= "# Moved pages rules\n";
        $lines = @file($custom_rewrite_fn);
        if (is_array($lines))
        {
            foreach ($lines as $line) {
                $line = trim($line);
                if (!strlen($line))
                    continue;

                $from_to = explode(EXP_SP, $line);
                if (count($from_to) != 2)
                {
                    xcms_log(XLOG_WARNING, "[XCMS:REWRITE] Line '$line' does not match rewrite rules");
                    continue;
                }

                $from = $from_to[0];
                $to = $from_to[1];
                $rewrite_text .= "RewriteCond %{QUERY_STRING} page=$from&?\$\n";
                $rewrite_text .= "RewriteRule .* index.php?page=$to\n";
            }
        }
        $rewrite_text .= "\n";
        $rewrite_text .= "# End of moved pages rules\n\n";
    }

    $custom_htaccess_fn = "${content_dir}cms/custom-htaccess";
    if (file_exists($custom_htaccess_fn))
    {
        $custom_contents = @file_get_contents($custom_htaccess_fn);
        $custom_contents = str_replace("@@CONTENT-PREFIX@", $content_dir, $custom_contents);
        $rewrite_text .= "# Custom htaccess rules\n";
        $rewrite_text .= $custom_contents;
        $rewrite_text .= "\n";
        $rewrite_text .= "# End of custom htaccess rules\n\n";
    }

    $rewrite_text .= "# Autogenerated rewrite rules from aliases\n";
    $aliases = xcms_get_aliases();
    $listing = array();
    $html_output .= "<table class=\"sitemap\">\n<tr><th>Alias</th><th>Path</th></tr>\n";
    ksort($aliases);
    $max_level = 0;
    foreach ($aliases as $alias => $path)
    {
        $level = substr_count($alias, "/");
        if ($level > $max_level)
            $max_level = $level;

        if (!array_key_exists($level, $listing))
            $listing[$level] = "";

        $listing[$level] .= "RewriteRule ^$alias$ index.php?page=$path\n";
        $listing[$level] .= "RewriteRule ^$alias/((.|\\r|\\n)*)$ index.php?page=$path&aparam=$1\n";

        $alias_str = str_replace('/', '<b class="slash">/</b>', $alias);
        $path_str = str_replace('/', '<b class="slash">/</b>', $path);
        $html_output .= "<tr><td>$alias_str</td><td>$path_str</td></tr>\n";
    }
    $html_output .= "</table>\n";

    for ($level = $max_level; $level >= 0; --$level)
    {
        if (!array_key_exists($level, $listing))
            continue;

        $rewrite_text .= $listing[$level];
    }

    if (!xcms_write(".htaccess", $rewrite_text))
    {
        $error = "Rewrite rules writing failed. ";
    }

    $html_output .= "<div class=\"notice\">Список alias-ов успешно обновлён</div>\n";

    return array(
        "output" => $html_output,
        "error" => $error,
    );
}

/**
  * Main method for rewrite rewrite rules after alias changes
  * @return dict("error", "output").
  * error can be either `false` or error message.
  **/
function xcms_rebuild_aliases_and_rewrite()
{
    $rebuild_aliases_result = xcms_rebuild_aliases();
    if ($rebuild_aliases_result !== true)
    {
        return array(
            "output" => "",
            "error" => "$rebuild_aliases_result Rewrite rules writing aborted. ",
        );
    }
    return _xcms_build_rewrite();
}
