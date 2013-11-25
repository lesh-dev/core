<?php
require_once("$engine_dir/sys/diff/diff-utils.php");

function xcms_process_page_diff($old_text, $new_text)
{
    global $web_prefix;

    // send notification only on non-trivial diffs
    if ($new_text === $old_text)
        return;

    $diff_html = xcms_diff_html($old_text, $new_text);
    $login = xcms_user()->login();
    $real_name = xcms_user()->param("name");
    $ifn = xcms_get_info_file_name();
    $page_info = xcms_get_list($ifn);
    $page_alias = xcms_get_key_or($page_info, 'alias');
    $url_name = $_SERVER["HTTP_HOST"]."/$web_prefix";
    $page_url = 'http://';
    $url_name .= (strlen($page_alias))
        ? $page_alias
        : '?'.xcms_url(array('page'=>$pageid));
    $page_url .= $url_name;
    $id = $page_alias;
    if (!strlen($id))
        $id = $pageid;
    $body_html = xcms_get_html_template("content-change");
    $body_html = str_replace('@@LOGIN@', $login, $body_html);
    $body_html = str_replace('@@REAL-NAME@', $real_name, $body_html);
    $body_html = str_replace('@@PAGE-ID@', $pageid, $body_html);
    $body_html = str_replace('@@PAGE-URL@', $page_url, $body_html);
    $body_html = str_replace('@@PAGE-ALIAS@', $url_name, $body_html);
    $body_html = str_replace('@@DIFF@', $diff_html, $body_html);
    // disable full page text
    //$body_html = str_replace('@@NEW-TEXT@', htmlspecialchars($new_text), $body_html);
    xcms_send_notification("content-change", NULL, $body_html);
}
?>