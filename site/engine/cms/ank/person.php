<?php

function xsm_get_vk_uid($social_profile)
{
    $match = array();
    // match id vk
    preg_match("/.*vk.com\/id([0-9]+)/", $social_profile, $match);
    if (count($match))
        return $match[1];

    // match id vkontakte
    preg_match("/.*vkontakte.ru\/id([0-9]+)/", $social_profile, $match);
    if (count($match))
        return $match[1];

    // match alias vk
    preg_match("/.*vk.com\/([A-Za-z._0-9]+)/", $social_profile, $match);
    if (count($match))
        return $match[1];

    // match alias vkontakte
    preg_match("/.*vkontakte.ru\/([A-Za-z._0-9]+)/", $social_profile, $match);
    if (count($match))
        return $match[1];

    return false;
}


function xsm_get_avatar($social_profile)
{
    // TODO: extract first profile (e.g. by spaces)
    // set default av
    global $full_engine_pub;
    $av = "${full_engine_pub}img/stalin50.jpg";
    $vk_uid = xsm_get_vk_uid($social_profile);
    if ($vk_uid === false)
        return $av;

    $cache_dir = ".prec/avatar-cache";
    @mkdir($cache_dir, 0777);

    $json_fn = "$cache_dir/vk-json-$vk_uid";
    $update_cache = false;
    if (file_exists($json_fn))
    {
        $fmt = @filemtime($json_fn);
        if ($fmt && time() - $fmt > 3600 * 24 * 14)
            $update_cache = true;
    }
    else
        $update_cache = true;

    $wget_cmd = "wget 'https://api.vk.com/method/getProfiles?uids=$vk_uid&fields=photo' -O $json_fn";
    if ($update_cache && (0 != system($wget_cmd)))
        return $av;

    $json_text = file_get_contents($json_fn);
    $json = @json_decode($json_text, true);
    if (!is_array($json))
        return $av;
    if (!array_key_exists('response', $json))
        return $av;
    $response = $json['response'];
    // VK returns empty array on invalid uid
    if (count($response) > 0)
    {
        $av = $response[0]['photo'];
    }
    return $av;
}
?>