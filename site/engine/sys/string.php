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

define('XU_YES', "yes");
define('XU_NO', "no");

/**
  * PHP 'empty' function replacement
  **/
function xu_empty($string)
{
    return strlen($string) == 0;
}

/**
  * PHP !empty function replacement
  **/
function xu_not_empty($string)
{
    return strlen($string) > 0;
}

/**
  * Get key value from list or return default value
  **/
function xcms_get_key_or($list, $key, $def_value = '')
{
    if (!array_key_exists($key, $list))
        return $def_value;
    $value = $list[$key];
    // special case for bool vars
    if (is_bool($def_value) || is_array($value))
        return $value;

    if (!strlen($value))
        return $def_value;
    return $value;
}


/**
  * Same as @c xcms_get_key_or but with encoding
  **/
function xcms_get_key_or_enc($list, $key, $def_value = '')
{
    return htmlspecialchars(xcms_get_key_or($list, $key, $def_value));
}

/**
  * Checks if user name is valid
  * @return true if user name is valid, false otherwise
  **/
function xcms_check_user_name($user_name)
{
    $result = array(
        "valid" => true,
    );
    if (xu_empty($user_name))
    {
        $result["valid"] = false;
        $result["reason"] = "Имя пользователя не может быть пустым. ";
        return $result;
    }

    // everything should be replaced if OK
    $bad = preg_replace("/[a-zA-Z0-9@._-]+/i", "", $user_name);
    if (!xu_empty($bad))
    {
        $result["valid"] = false;
        $result["reason"] = "Имя пользователя содержит недопустимые символы. ";
    }

    // Check that first letter kosherity
    $letters = preg_replace("/[^a-zA-Z0-9]+/i", "", xu_substr($user_name, 0, 1));
    if (xu_empty($letters))
    {
        $result["valid"] = false;
        $result["reason"] = "Имя пользователя должно начинаться с буквы или цифры. ";
        return $result;
    }

    return $result;
}

/**
  * Checks whether page id is valid
  * @return true if page id is valid, false otherwise
  **/
function xcms_check_page_id($page_id, $local = false)
{
    // everything should be replaced if OK
    $bad = preg_replace("#[a-z/A-Z.0-9_-]+#", "", $page_id);
    if (!xu_empty($bad))
        return false;

    // forbid duplicated dots
    if (strpos($page_id, "..") !== false)
        return false;

    if (xu_empty($page_id))
        return false;

    if ($local && strpos($page_id, "/") !== false)
        return false;

    return true;
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
  * Filters all non-digits from string
  * @return filtered string
  **/
function xcms_filter_nondigits($string)
{
    return preg_replace('/[^0-9-]/', "", $string);
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
  **/
function xu_substr($string, $start, $length = false)
{
    if ($length === false)
        $length = xu_len($string) - $start;
    return mb_substr($string, $start, $length, 'UTF-8');
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
  * Python x.startswith(y) analogue.
  **/
function xu_startswith($string, $substring)
{
    return (mb_substr($string, 0, xu_len($substring), 'UTF-8') === $substring);
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
function xu_transliterate($string)
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

function xcms_truncate_text($text, $limit, $trail)
{
    if ($limit <= 0 || xu_len($text) <= $limit)
        return $text;

    $text = xu_substr($text, 0, $limit);
    $n = xu_len($text);
    for ($i = $n - 1; $i >= 0; $i--)
    {
        if (xu_substr($text, $i, 1) == EXP_SP)
        {
            $text = xu_substr($text, 0, $i);
            break;
        }
    }
    return trim($text).$trail;
}

function xcms_truncate_hypertext($text, $limit, $trail)
{
    $text = preg_replace("/\<\?php.*?\?>/", '', $text);
    // FIXME(mvel): proper logging
    xcms_log(0, "===========\n$text\n--------------");
    return xcms_truncate_text($text, $limit, $trail);
}

define('MAX_LENGTH_DEFAULT', 160);

function xcms_wrap_long_lines($text, $max_length = MAX_LENGTH_DEFAULT)
{
    $text = trim($text);
    $lines = explode(EXP_LF, $text);
    $new_lines = array();
    foreach ($lines as $ln)
    {
        $ln = str_replace(EXP_CR, '', $ln);
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
            $ln = trim(xu_substr($ln, $pos));
        }
        // add rest of line
        $new_lines[] = $ln;
    }
    return implode(EXP_LF, $new_lines);
}

/**
  * Translate page title/etc to string that can be used
  * as page path component or as alias
  **/
function xcms_to_valid_filename($title)
{
    $title_tr = strtr(strtolower(xu_transliterate($title)), " _/", "---");
    $title_tr = preg_replace("/[^0-9a-zA-Z-]/", "", $title_tr);
    $title_tr = preg_replace("/[-]{2,}/", "-", $title_tr);
    $title_tr = substr($title_tr, 0, 50);
    return $title_tr;
}

/**
  * String library unit test
  **/
function xcms_string_unit_test()
{
    xut_begin("string");

    // test generic PHP weird things
    xut_check(0 == "", "Zero is weak-equal to empty string");
    xut_check(0 !== "", "Zero is not weak-equal to empty string");
    xut_check((string)(0) === "0", "Zero directly converted to string is a '0'");
    xut_check((string)(0) != (string)(""), "Zero converted to string is not any empty string");

    // test xcms_get_key_or function
    $obj = array();
    $obj["super"] = 1;
    $obj["pupper"] = false;
    $obj["zero-value"] = 0;
    $obj["another"] = "test string";
    $obj["empty"] = "";
    $obj["need_escaping"] = "&";
    $obj["array"] = array("qqq" => true);
    $obj["empty-array"] = array();

    xut_equal(xcms_get_key_or($obj, "super"), 1, "Invalid 'super' key");
    xut_equal(xcms_get_key_or($obj, "pupper", true), false, "Invalid 'pupper' key");
    xut_equal(xcms_get_key_or($obj, "zero-value"), 0, "Invalid 'zero-value' key");
    xut_equal(xcms_get_key_or($obj, "another"), "test string", "Invalid 'another' key");
    xut_equal(xcms_get_key_or($obj, "empty"), "", "Invalid 'empty' key");
    xut_equal(xcms_get_key_or($obj, "empty", "some"), "some", "Failed empty value key test");
    xut_equal(xcms_get_key_or($obj, "missing"), "", "Failed missing key test");
    xut_equal(xcms_get_key_or($obj, "missing-bool", true), true, "Failed missing bool key");
    xut_equal(xcms_get_key_or($obj, "pupper", true), false, "Failed existing bool key");

    xut_equal(xcms_get_key_or_enc($obj, "need_escaping"), "&amp;", "Failed get key with escaping");

    $array_value = xcms_get_key_or($obj, "array");
    xut_check(is_array($array_value), "Array value type");
    xut_check($array_value["qqq"] === true, "Array value");

    $empty_obj = array();
    $def_key_value = xcms_get_key_or($empty_obj, "nokey", array());
    xut_check(is_array($def_key_value) , "Failed array default value type");
    xut_check(count($def_key_value) == 0, "Failed array default value item count");

    $def_key_value = xcms_get_key_or($empty_obj, "nokey", array("qqq" => true));
    xut_check(is_array($def_key_value) , "Failed non-empty array default value type");
    xut_check($def_key_value["qqq"] === true, "Failed non-empty array default value items");

    xut_check(xu_not_empty(0), "Zero is empty");
    xut_check(xu_empty(""), "Empty string is not empty");

    xut_equal(xcms_filter_nondigits("100; drop database"), "100", "Non-digits filtering failed");

    // xcms_check_user_name
    $valid_user0 = xcms_check_user_name("vasya.123");
    $valid_user1 = xcms_check_user_name("vasya@123.com");
    $valid_user2 = xcms_check_user_name("vasya_pupkin");

    $invalid_user0 = xcms_check_user_name(".");
    $invalid_user1 = xcms_check_user_name("..");
    $invalid_user2 = xcms_check_user_name("...");
    $invalid_user3 = xcms_check_user_name("../usr/vasya");
    $invalid_user4 = xcms_check_user_name(".vasya");

    xut_check($valid_user0["valid"], "Check valid user 0");
    xut_check($valid_user1["valid"], "Check valid user 1");
    xut_check($valid_user2["valid"], "Check valid user 2");

    xut_check(!$invalid_user0["valid"], "Check invalid user 0");
    xut_check(!$invalid_user1["valid"], "Check invalid user 1");
    xut_check(!$invalid_user2["valid"], "Check invalid user 2");
    xut_check(!$invalid_user3["valid"], "Check invalid user 3");
    xut_check(!$invalid_user4["valid"], "Check invalid user 4");

    // xcms_check_password
    xut_check(xcms_check_password("123@#$%^&abcABC bla\xFE\xFF"), "Check valid password");
    xut_check(!xcms_check_password("\n\taa\rbb\0\\'qqq'+\"zzz"), "Check invalid password");

    xut_equal(xu_len("Привет000"), 9, "Check xu_len");
    xut_equal(xu_strpos("Привет000", "т00", 0), 5, "Check xu_strpos");
    xut_equal(xu_substr("Привет000", 3, 3), "вет", "Check xu_substr");
    xut_equal(xu_substr("Привет000", 3), "вет000", "Check xu_substr with optional length");

    xut_equal(xu_strspn("альфаКу", "афьл", 1), 4, "Check xu_strspn");
    xut_equal(xu_strcspn('abcd', 'apple'), 0, "Check xu_strcspn one");
    xut_equal(xu_strcspn('abcd', 'banana'), 0, "Check xu_strcspn two");
    xut_equal(xu_strcspn('heЛЛo', 'Л'), 2, "Check xu_strcspn three");
    xut_equal(xu_strcspn('heЛЛo', 'ДworЛЛd'), 2, "Check xu_strcspn four");

    xut_equal(xu_startswith("0иван0 человеков", "0ива"), true, "Check xu_startswith");

    xut_equal(xcms_wrap_long_lines("  Очень длинный текст, который надо перенести\n\n\n", 20),
        "Очень длинный\nтекст, который надо\nперенести", "Check xcms_wrap_long_lines");

    xut_equal(xcms_wrap_long_lines("  Очень длинный текст, который надо перенести\n\nне\nсмотря\nни\nна что", 20),
        "Очень длинный\nтекст, который надо\nперенести\n\nне\nсмотря\nни\nна что", "Check xcms_wrap_long_lines");

    xut_equal(xu_transliterate("Вельтищев Михаил"), "Veltischev Mihail", "Check xu_transliterate");

    $trunc_text =
        "Иван  Человеков был простой человек и просто смотрел на свет, ".
        "И <<да>> его было настоящее <<да>>, а нет~--- настоящее <<нет>>";
    xut_equal(xcms_truncate_text($trunc_text, 300, " ..."), $trunc_text, "Check xcms_truncate_text 0");
    xut_equal(xcms_truncate_text($trunc_text, 10, " ..."), "Иван ...", "Check xcms_truncate_text 1");
    xut_equal(xcms_truncate_text($trunc_text, 20, " ..."), "Иван  Человеков был ...", "Check xcms_truncate_text 2");

    $trunc_hypertext =
        "<?php qqq(); ?>Иван  Человеков был простой человек и просто смотрел на свет, ".
        "И <<да>> его было настоящее <<да>>, а нет~--- настоящее <<нет>>";
    $trunc_hypertext_cut =
        "Иван  Человеков был простой человек и просто смотрел на свет, ".
        "И <<да>> его было настоящее <<да>>, а нет~--- настоящее <<нет>>";
    xut_equal(xcms_truncate_hypertext($trunc_hypertext, 300, " ..."), $trunc_hypertext_cut, "Check xcms_truncate_hypertext 0");
    xut_equal(xcms_truncate_hypertext($trunc_hypertext, 10, " ..."), "Иван ...", "Check xcms_truncate_hypertext 1");

    xut_equal(
        xcms_to_valid_filename("26 апреля ЛЭШевцы идут  на озеро!?"),
        "26-aprelya-leshevcy-idut-na-ozero",
        "Check xcms_to_valid_filename");

    xut_end();
}
?>
