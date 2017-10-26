<?php
require_once("${xengine_dir}sys/diff/diff-utils.php");
require_once("${xengine_dir}sys/template.php");

function xcms_process_page_diff($old_text, $new_text, $page_id = false)
{
    global $web_prefix;

    // send notification only on non-trivial diffs
    if ($new_text === $old_text)
        return;

    $diff_html = xcms_diff_html($old_text, $new_text);
    $ifn = xcms_get_info_file_name($page_id);
    $page_info = xcms_get_list($ifn);
    $page_alias = xcms_get_key_or($page_info, 'alias');
    $url_name = $_SERVER["HTTP_HOST"]."/$web_prefix";
    $page_url = 'http://';
    if ($page_id === false)
    {
        global $pageid;
        $page_id = $pageid;
    }
    $url_name .= (strlen($page_alias))
        ? $page_alias
        : '?'.xcms_url(array('page' => $page_id));
    $page_url .= $url_name;
    $id = $page_alias;
    if (!strlen($id))
        $id = $page_id;

    $body_html = xcms_prepare_html_template("content-change");
    $body_html = str_replace('@@PAGE-ID@', $page_id, $body_html);
    $body_html = str_replace('@@PAGE-URL@', $page_url, $body_html);
    $body_html = str_replace('@@PAGE-ALIAS@', $url_name, $body_html);
    $body_html = str_replace('@@DIFF@', $diff_html, $body_html);
    // disable full page text
    //$body_html = str_replace('@@NEW-TEXT@', htmlspecialchars($new_text), $body_html);
    xcms_send_notification("content-change", NULL, $body_html);

    return $diff_html;
}
?>