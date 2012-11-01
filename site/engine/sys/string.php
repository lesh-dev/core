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

    /**
      * Returns length in UTF-8 characters
      * It's just a simple wrapper around mb_strlen
      **/
    function xcms_len($string)
    {
        return mb_strlen($string, 'UTF-8');
    }

    /**
      * String library unit test
      **/
    function xcmsut_string()
    {
        $r = true;
        $r = $r && (xcms_filter_password("\n\taa\rbb\0\\'qqq'+\"zzz") == "aabb\\'qqq'+\"zzz");
        $r = $r && (xcms_len("Привет000") == 8);
        return $r;
    }
?>
