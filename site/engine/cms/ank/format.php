<?php
require_once("${engine_dir}sys/db.php");
require_once("${engine_dir}cms/ank/fio.php");

define('XSM_CONTACT_SEPARATOR', ',&nbsp;&nbsp; ');
define('XSM_SCHOOL_COUNT', 7);  // not used by now

/**
  * Replace \n by <br /> with respect to various systems line endings
  **/
function xcms_html_wrap_by_crlf($html)
{
    // detect UNIX or DOS line-endings
    if (strpos($html, "\n") !== false)
    {
        // Unix or DOS, so \n -> <br />, '\r' -> void
        $html = str_replace("\n", "<br />", $html);
        $html = str_replace("\r", "", $html);
    }
    elseif (strpos($html, "\r") !== false)
    {
        // MacOS, \r only
        $html = str_replace("\r", "<br />", $html);
    }
    return $html;
}

/**
  * Prepend one <br /> when HTML code already contains some
  **/
function xcms_html_wrap_ml($html)
{
    if (strpos($html, "<br />")) $html = "<br />$html";
    return $html;
}


function xcms_trim_object($obj)
{
    $new_obj = array();
    foreach ($obj as $key=>$value)
    {
        $new_obj[$key] = trim($value);
    }
    return $new_obj;
}

/**
  * Plural form for nouns
  **/
function xcms_plural($n, $word)
{
    if ($n  % 10 == 1)
        return "${word}";

    if ($n  % 10 >= 2 && $n % 10 <= 4)
        return "${word}а";

    return "${word}ов";
}

/**
  * Get class number without any trash after
  **/
function xsm_class_num($class)
{
    if (!preg_match("/^[0-9]+/", $class))
        return $class;
    return preg_replace("/^([0-9]+).*/", "\\1", $class);
}

/**
  * Process human-usable timestamp without seconds
  * with non-breaking spaces inside.
  * @param $timestamp should be in format used in in DBMS,
  * i.e. YYYY.MM.DD HH:MM:SS
  **/
function xsm_ymdhm($timestamp)
{
    if (strlen($timestamp) != 19)
        return $timestamp;
    $timestamp = substr($timestamp, 0, 16);
    //$timestamp = str_replace(' ', '&nbsp;', $timestamp);
    return $timestamp;
}

/**
  * Link highligter for comments
  * Return properly quoted html
  **/
function xsm_highlight_links($text)
{
    $result = "";
    $cur_pos = 0;
    while (true)
    {
        $p = strpos($text, "http://", $cur_pos);
        $ps = strpos($text, "https://", $cur_pos);
        if ($p !== false && $ps !== false)
            $p = min($p, $ps);
        elseif ($p !== false)
            $p = $p;  // do nothing
        elseif ($ps !== false)
            $p = $ps;
        else
            break;

        $result .= htmlspecialchars(substr($text, $cur_pos, $p - $cur_pos));
        $link_length = strcspn($text, "\r\n\t, ", $p);
        $link = substr($text, $p, $link_length);
        // cut a dot if it is a link trail (more likely it is a sentence end)
        if (substr($link, $link_length - 1) == ".")
        {
            $link_length--;
            $link = substr($link, 0, $link_length);
        }
        $result .= "<a href=\"$link\">$link</a>";
        $cur_pos = $p + $link_length;
    }
    $result .= htmlspecialchars(substr($text, $cur_pos));
    return $result;
}

/**
  * Parses phones string (allowed format is comma-separated)
  * Returns list of parsed items (one item on parse error)
  **/
function xsm_format_phones($phones_str)
{
    $phones_str = str_replace("\r", " ", $phones_str);
    $phones_str = str_replace("\n", " ", $phones_str);
    $phones_str = str_replace("\t", " ", $phones_str);
    $phones_str = trim($phones_str);

    $result = array();
    if (xu_empty($phones_str))
        return $result;

    if (preg_match("/[^0-9()+, -]/", $phones_str))
    {
        // something strange here, cannot format
        $item = array(
            "phone"=>$phones_str,
            "hint"=>"В телефонах допустимы только символы 0-9 ( ) + - и пробел. ",
            "valid"=>false
        );
        $result[] = $item;
        return $result;
    }

    $phones = explode(',', $phones_str);
    for ($i = 0; $i < count($phones); ++$i)
    {
        $phone = trim($phones[$i]);
        $item = array(
            "valid"=>true,
            "hint"=>"",
            "phone"=>$phone
        );

        // check digit count
        $digits = preg_replace("/[^0-9]/", "", $phone);
        if (strlen($digits) != 11)
        {
            // don't know how to format this
            $item["hint"] = "Телефон должен содержать 11 цифр. ";
            $item["valid"] = false;
            $result[] = $item;
            continue;
        }
        $item["digits"] = $digits;

        if ($digits[0] == "7")
            $digits[0] = "8"; // fix country code

        $cl = false;
        if (substr($digits, 0, 2) == "89" ||
            substr($digits, 0, 4) == "8495" ||
            substr($digits, 0, 4) == "8499")
            $cl = 3;
        else
        {
            $r = array();
            if (!preg_match("/\([0-9]+\)/", $phone, $r))
            {
                // cannot parse code
                $item["hint"] = "Код города должен быть обрамлён скобками. ";
                $item["valid"] = false;
                $result[] = $item;
                continue;
            }
            $cl = strlen($r[0]) - 2;

            if ($cl < 3 || $cl > 5)
            {
                // invalid area code
                $item["hint"] = "Код города должен содержать от 3 до 5 цифр. ";
                $item["valid"] = false;
                $result[] = $item;
                continue;
            }
        }
        $phone = substr($digits, 0, 1).'<span class="pb">(</span>'.substr($digits, 1, $cl).'<span class="pb">)</span>';
        if ($cl == 3)
            $phone .= substr($digits, 4, 3).'-'.substr($digits, 7, 2).'-'.substr($digits, 9, 2);
        elseif ($cl == 4)
            $phone .= substr($digits, 5, 2).'-'.substr($digits, 7, 2).'-'.substr($digits, 9, 2);
        else // ($cl == 5)
            $phone .= substr($digits, 6, 2).'-'.substr($digits, 8, 3);

        $item["phone"] = $phone;
        $item["hint"] = $phones[$i];
        $result[] = $item;
    }
    return $result;
}

/**
  * Format phone string using @c xsm_format_phones
  * to HTML output
  **/
function xsm_make_phone($phones_str, $id = '')
{
    $items = xsm_format_phones($phones_str);
    if (!count($items))
        return "";

    $result = "";
    $count = 0;
    foreach ($items as $item)
    {
        $hint = $item["hint"];
        $valid = $item["valid"];
        $phone = $item["phone"];
        $class = "";
        if (!$valid)
        {
            $class = "error";
            $phone = htmlspecialchars($phone);
        }
        if (xu_not_empty($result))
            $result .= XSM_CONTACT_SEPARATOR;

        $pid = xu_not_empty($id) ? " id=\"$id-$count\" " : "";
        $result .= "<span $pid class=\"phone $class\" title=\"$hint\">$phone</span>";
        ++$count;
    }
    return $result;
}

function xsm_make_phone_from_obj($obj, $table_name, $key)
{
    $id = xcms_get_key_or($obj, "${table_name}_id");
    return xsm_make_phone(xcms_get_key_or($obj, $key), "$table_name$id-$key");
}

/**
  * Final formatting for all person phones into one HTML string
  **/
function xsm_format_person_phones($person)
{
    $phone = xsm_make_phone_from_obj($person, "person", "phone");
    $cellular = xsm_make_phone_from_obj($person, "person", "cellular");
    $all_phones = array();
    if ($cellular)
        $all_phones[] = $cellular;
    if ($phone)
        $all_phones[] = $phone;
    return implode(XSM_CONTACT_SEPARATOR, $all_phones);
}

function xsm_contacts_for_list($person)
{
    $all_phones = trim(xsm_format_person_phones($person));
    $skype = xcms_get_key_or_enc($person, "skype");
    $email = xcms_get_key_or_enc($person, "email");
    $social_profile = xsm_prepare_social_profile($person["social_profile"]);

    $contacts = array();
    if (xu_not_empty($all_phones))
        $contacts[] = $all_phones;
    if (xu_not_empty($skype) && count($contacts) < 3)
        $contacts[] = $skype;
    if (xu_not_empty($email) && count($contacts) < 3)
        $contacts[] = "<a href=\"mailto:$email\">$email</a>";
    if (xu_not_empty($social_profile) && count($contacts) < 3)
        $contacts[] = xsm_social_profile_link($social_profile);

    return implode(XSM_CONTACT_SEPARATOR, $contacts);
}

function xsm_prepare_social_profile($social_profile)
{
    // make it valid URL if it was it form example.com/name
    if (xu_not_empty($social_profile) &&
        strpos(substr($social_profile, 0, 8), '://') === false) // http/https scheme not matched
        $social_profile = "http://$social_profile"; // assume http scheme
    $social_profile = htmlspecialchars($social_profile);
    return $social_profile;
}

// TODO: when profile is a VK link, transform it into VK icon
function xsm_social_profile_link($social_profile)
{
    $title = $social_profile;
    $title = str_replace("http://", "", $title);
    $title = str_replace("https://", "", $title);
    return "<a target=\"_blank\" href=\"$social_profile\">$title</a>";
}

/**
  * id is added for testability reasons
  **/
function xsm_make_enum($object, $key, $id = false)
{
    $enum_value = xsm_check_enum_key($key, $object[$key]);
    $css_class = str_replace('_', '-', $key);
    $values = xsm_get_enum($key);
    $title = $values[$enum_value];
    $id = ($id !== false) ? "$id-" : "";
    return "<span class=\"$css_class xe-$enum_value\" id=\"$id$key-span\">$title</span>";
}

function xsm_calc_course_style($course_ratio)
{
    if ($course_ratio >= -0.001 && $course_ratio < 0.333)
        return "xe-low";
    elseif ($course_ratio >= 0.333 && $course_ratio < 0.666)
        return "xe-medium";
    elseif ($course_ratio >= 0.666 && $course_ratio < 0.999)
        return "xe-high";
    elseif ($course_ratio >= 0.999)
        return "xe-all";
    return "xe-undef";
}

/**
  * Non-generic function, see xsm_make_enum
  * id is added for testability reasons
  **/
function xsm_make_forest_enum($person, $fn, $id = false)
{
    $id = ($id !== false) ? "$id-" : "";
    $forest_status = xsm_check_enum_key("forest_status", $person["forest_$fn"]);
    $values = xsm_get_enum("forest_status");
    $title = $values[$forest_status];
    return "<span class=\"forest-status $forest_status\" id=\"${id}forest_status$fn-span\">$title</span>";
}

function xsm_person_list_link($school_id)
{
    $school = xdb_get_entity_by_id('school', $school_id);
    $school_title = xcms_get_key_or_enc($school, 'school_title');
    $school_url = "list-person".xcms_url(array('school_id'=>$school_id));
    return "<a href=\"$school_url\">$school_title</a>";
}

function xsm_person_view_link($person_id, $school_id, $title_ht = "")
{
    if (xu_empty($title_ht))
    {
        $person = xdb_get_entity_by_id('person', $person_id);
        $title_ht = xsm_fi_enc($person);
    }
    $person_url = "view-person".xcms_url(array('person_id'=>$person_id, 'school_id'=>$school_id));
    return "<a href=\"$person_url\">$title_ht</a>";
}

function xsm_draw_fio_filter()
{
    ?><span class="ankListField">Фильтр ФИО:</span>
    <input class="ankEdit filter" type="text"
        value="<?php echo xcms_get_key_or_enc($_POST, 'show_name_filter'); ?>"
        name="show_name_filter" id="show_name_filter-input"
        title="Будут найдены все участники, в ФИО которых (в любом порядке) встречаются слова запроса,
        без учёта регистра. Например, 'дан Мих' найдёт Даниила Михайловича, Михаила Данилевского
        и Богдана Немихульского, но НЕ найдёт Мишу Данилкина (имена условны)" /><?php
}

/**
  * @param table_name Table to fetch from
  * @param name HTML element name (and post key)
  * @param current_key Current vey value (pre-selected)
  * @param title_keys What keys use to form element titles
  * @param aux_cond Condition to pass in WHERE clause
  * @param attr HTML attributes for SELECT element
  * @param special if not false, add special element to the top of the list
  *     with XDB_INVALID_ID key value
  **/
function xsm_make_selector($table_name, $name, $current_key, $title_keys, $aux_cond = '', $attr = '', $special = false)
{
    $db = xdb_get();
    $query = "SELECT * FROM $table_name";
    if (strlen($aux_cond))
        $query .= " WHERE $aux_cond";
    $sel = $db->query($query);
    $html = "<select name=\"$name\" id=\"$name-selector\" $attr>\n";
    $list_key = "${table_name}_id";
    $special_value = XDB_INVALID_ID;
    if ($special !== false)
    {
        $selected = ("" == $current_key) ? 'selected="selected"' : '';
        $html .= "<option $selected value=\"$special_value\">$special</option>\n";
    }
    while ($object = $sel->fetchArray(SQLITE3_ASSOC))
    {
        $title = "";
        foreach ($title_keys as $key_name)
            $title .= $object[$key_name].' ';
        $title = htmlspecialchars(trim($title));
        $key = $object[$list_key];
        $selected = ($key == $current_key) ? 'selected="selected"' : '';
        $html .= "<option $selected value=\"$key\">$title</option>\n";
    }
    $html .= "</select>";
    $db->close();
    return $html;
}

/**
  * Builds selector HTML element from SQL data
  * @param $list_key key name to use as option ids
  * @param $name select HTML name
  * @param $current_key selected key value
  * @param $title_pattern string with @@key@ patterns
  * that will be replaced by values taken from database
  * @example "@@book_title@ - @@author_name"
  * @param $query SQL statement to get data
  * @param $attr auxillary attributes passed to SELECT element (empty by default)
  **/
function xsm_make_selector_ext($list_key, $name, $current_key, $title_pattern, $query, $attr = '', $exclude_ids = array())
{
    $db = xdb_get();
    $sel = $db->query($query);
    $html = "<select name=\"$name\" id=\"$name-selector\" $attr>\n";
    $uniq_titles = array();
    while ($object = $sel->fetchArray(SQLITE3_ASSOC))
    {
        $title = $title_pattern;
        foreach ($object as $key => $value)
            $title = str_replace("@@$key@", htmlspecialchars($value), $title);
        $uniq_title = $title;
        foreach ($object as $key => $value)
            $title = str_replace("##$key#", htmlspecialchars($value), $title);
        foreach ($object as $key => $value)
            $uniq_title = str_replace("##$key#", "", $uniq_title);

        if (array_key_exists($uniq_title, $uniq_titles))
            continue;
        $uniq_titles[$uniq_title] = true;

        $key = $object[$list_key];
        if (xcms_get_key_or($exclude_ids, $key))
            continue;
        $selected = ($key == $current_key) ? 'selected="selected"' : '';
        $html .= "<option $selected value=\"$key\">$title</option>\n";
    }
    $html .= "</select>";
    $db->close();
    return $html;
}

function xsm_make_enum_selector($name, $value, $items)
{
    $html = "<select name=\"$name\" id=\"$name-selector\">\n";
    foreach ($items as $key => $title)
    {
        $sel = ($key == $value) ? ' selected="selected" ' : '';
        $html .= "<option $sel value=\"$key\">$title</option>\n";
    }
    $html .= "</select>";
    return $html;
}

function xsm_checkbox($name, $value)
{
    xcmst_control($name, $value, "", "ankEdit", "checkbox", "");
}

function xsm_field($table_name, $key)
{
    $fields_desc = xsm_get_fields($table_name);
    $desc = $fields_desc[$key];
    ?><span class="xsm-fixed-field"><?php echo $desc["name"]; ?></span> <?php
}
?>