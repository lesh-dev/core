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
      * Replaces Russian UTF-8 symbols to ANSI transliteration
      * @param string string to transliterate
      * @return transliterated string
      **/
    function xcms_transliterate($string)
    {
        $converter = array(
            'а' => 'a',   'б' => 'b',   'в' => 'v',
            'г' => 'g',   'д' => 'd',   'е' => 'e',
            'ё' => 'e',   'ж' => 'zh',  'з' => 'z',
            'и' => 'i',   'й' => 'y',   'к' => 'k',
            'л' => 'l',   'м' => 'm',   'н' => 'n',
            'о' => 'o',   'п' => 'p',   'р' => 'r',
            'с' => 's',   'т' => 't',   'у' => 'u',
            'ф' => 'f',   'х' => 'h',   'ц' => 'c',
            'ч' => 'ch',  'ш' => 'sh',  'щ' => 'sch',
            'ь' => '',    'ы' => 'y',   'ъ' => '',
            'э' => 'e',   'ю' => 'yu',  'я' => 'ya',

            'А' => 'A',   'Б' => 'B',   'В' => 'V',
            'Г' => 'G',   'Д' => 'D',   'Е' => 'E',
            'Ё' => 'E',   'Ж' => 'Zh',  'З' => 'Z',
            'И' => 'I',   'Й' => 'Y',   'К' => 'K',
            'Л' => 'L',   'М' => 'M',   'Н' => 'N',
            'О' => 'O',   'П' => 'P',   'Р' => 'R',
            'С' => 'S',   'Т' => 'T',   'У' => 'U',
            'Ф' => 'F',   'Х' => 'H',   'Ц' => 'C',
            'Ч' => 'Ch',  'Ш' => 'Sh',  'Щ' => 'Sch',
            'Ь' => '',    'Ы' => 'Y',   'Ъ' => '',
            'Э' => 'E',   'Ю' => 'Yu',  'Я' => 'Ya',
        );
        $string = strtr($string, $converter);
        return $string;
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
        xut_check(xcms_transliterate("Вельтищев Михаил") == "Veltischev Mihail", "Check xcms_transliterate");
        xut_end();
    }
?>
