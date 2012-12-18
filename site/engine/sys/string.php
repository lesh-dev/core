<?php
    /**
      * String library, user input filtering, etc
      * Maintainer: mvel@
      **/

    /**
      * Checks if user name is valid
      * @return true if user name is valid, false otherwise
      **/
    function xcms_check_user_name($user_name)
    {
        // everything should be replaced if OK
        $bad = preg_replace("/[a-zA-Z0-9@._-]+/i", "", $user_name);
        return empty($bad);
    }

    /**
      * Checks if password consists of valid characters
      * @param password to check
      * @return true if valid, false otherwise
      **/
    function xcms_check_password($password)
    {
        // no characters should be replaced
        return ($password == preg_replace('/[\x00-\x1F]/', "", $password));
    }

    /**
      * Filters all non-printable characters from string
      * @return filtered string
      **/
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
    function xcms_string_unit_test()
    {
        xut_begin("xcms_string");
        xut_check(xcms_check_password("123@#$%^&abcABC bla\xFE\xFF"), "Check valid password");
        xut_check(!xcms_check_password("\n\taa\rbb\0\\'qqq'+\"zzz"), "Check invalid password");
        xut_check(xcms_len("Привет000") == 9, "Check xcms_len");
        xut_end();
    }
?>
