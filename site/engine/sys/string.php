<?php
    /* String library */

    function xcms_filter_user_name($user_name)
    {
        return preg_replace("/[^a-zA-Z0-9._-]/", "", $user_name);
    }

    function xcms_filter_password($passwd)
    {
        return preg_replace('/[\x0A\x0D\x09\x00]/', "", $passwd);
    }

    function xcms_filter_nonchars($string)
    {
        return preg_replace('/[\x00-\x1F]/', "", $string);
    }

    /* Unit test */
    function xcmsut_filter_password()
    {
        return xcms_filter_password("\n\taa\rbb\0\\'qqq'+\"zzz") == "aabb\\'qqq'+\"zzz";
    }

?>
