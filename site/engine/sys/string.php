<?php
    /**
      * String library, user input filtering, etc
      * Maintainer: mvel@
      **/

    define('EXP_LF', "\n");
    define('EXP_CR', "\r");
    define('EXP_CRLF', "\r\n");

    define('EXP_SP', ' ');
    define('EXP_SL2', '//');
    define('EXP_EQ', '=');
    define('EXP_COL', ':');
    define('EXP_PIPE', '|');
    define('EXP_COM', ',');

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
    function xu_len($string)
    {
        return mb_strlen($string, 'UTF-8');
    }

    /**
      * Cuts a substring from UTF-8 string
      * It's just a simple wrapper around mb_substr
      * @sa xcms_end
      **/
    function xu_substr($string, $start, $length)
    {
        return mb_substr($string, $start, $length, 'UTF-8');
    }

    /**
      * Cuts a substring from UTF-8 string up to the end
      * It's just a simple wrapper around mb_substr
      * @sa xu_substr
      **/
    function xu_end($str, $start) {
        return mb_substr($str, $start, xu_len($str) - $start, 'UTF-8');
    }

    /**
      * Returns char-based substring position (UTF-8)
      * It's just a simple wrapper around @c mb_strpos
      **/
    function xu_strpos($haystack, $needle, $offset = 0)
    {
        return mb_strpos($haystack, $needle, $offset, 'UTF-8');
    }

    /**
      * Split string to array of UTF-8 characters
      **/
    function xu_split($str)
    {
        return preg_split("//u", $str, -1, PREG_SPLIT_NO_EMPTY);
    }

    function xu_strspn($str, $pattern, $start = 0)
    {
        $pos = 0;
        while (true)
        {
            $sym = xu_substr($str, $start + $pos, 1);
            if (!strlen($sym))
                break;
            if (xu_strpos($pattern, $sym) === false)
                break;
            ++$pos;
        }
        return $pos;
    }

    function xu_strcspn($str, $pattern, $start = 0)
    {
        $pos = 0;
        while (true)
        {
            $sym = xu_substr($str, $start + $pos, 1);
            if (!strlen($sym))
                break;
            if (xu_strpos($pattern, $sym) !== false)
                break;
            ++$pos;
        }
        return $pos;
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

    define('MAX_LENGTH_DEFAULT', 160);

    function xcms_wrap_long_lines($text, $max_length = MAX_LENGTH_DEFAULT)
    {
        $lines = explode(EXP_LF, $text);
        $new_lines = array();
        foreach ($lines as $ln)
        {
            $ln = str_replace(EXP_CR, "", $ln);
            if (xu_len($ln) < $max_length)
            {
                $new_lines[] = $ln;
                continue;
            }
            // split long line into short lines
            while (xu_len($ln) >= $max_length)
            {
                $pos = $max_length - 1;
                while ($pos)
                {
                    if (xu_substr($ln, $pos, 1) != ' ')
                    {
                        $pos--;
                        continue;
                    }
                    break;
                }

                if (!$pos) // cannot split
                    break;

                // split char found
                $cut = trim(xu_substr($ln, 0, $pos));
                $new_lines[] = $cut;
                $ln = trim(xu_end($ln, $pos));
            }
            // add rest of line
            $new_lines[] = $ln;
        }
        return implode(EXP_LF, $new_lines);
    }

    /**
      * String library unit test
      **/
    function xcms_string_unit_test()
    {
        xut_begin("xcms_string");
        xut_check(xcms_check_password("123@#$%^&abcABC bla\xFE\xFF"), "Check valid password");
        xut_check(!xcms_check_password("\n\taa\rbb\0\\'qqq'+\"zzz"), "Check invalid password");

        xut_check(xu_len("Привет000") == 9, "Check xu_len");
        xut_check(xu_strpos("Привет000", "т00", 0) == 5, "Check xu_strpos");
        xut_check(xu_substr("Привет000", 3, 3) == "вет", "Check xu_substr");

        xut_check(xu_strspn("альфаКу", "афьл", 1) === 4, "Check xu_strspn");
        xut_check(xu_strcspn('abcd', 'apple') === 0, "Check xu_strcspn one");
        xut_check(xu_strcspn('abcd', 'banana') === 0, "Check xu_strcspn two");
        xut_check(xu_strcspn('heЛЛo', 'Л') === 2, "Check xu_strcspn three");
        xut_check(xu_strcspn('heЛЛo', 'ДworЛЛd') === 2, "Check xu_strcspn four");

        xut_check(xcms_wrap_long_lines('Очень длинный текст, который надо перенести', 20) ===
            "Очень длинный\nтекст, который надо\nперенести", "Check xcms_wrap_long_lines");

        xut_check(xcms_transliterate("Вельтищев Михаил") == "Veltischev Mihail", "Check xcms_transliterate");
        xut_end();
    }
?>
