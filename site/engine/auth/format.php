<?php
global $engine_dir;
global $xengine_dir;
require_once("${xengine_dir}sys/groups.php");
require_once("${xengine_dir}sys/db.php");
require_once("${engine_dir}xsm/user.php");
require_once("${engine_dir}cms/ank/fio.php");
require_once("${engine_dir}cms/ank/field-desc.php");

define('XDP_NORMAL', 1);
define('XDP_READONLY', 2);
define('XDP_COMPACT', 3);

function xcmst_draw_privileges($user, $mode = XDP_NORMAL)
{
    if ($mode != XDP_COMPACT)
    {?>
        <h3>Привилегии</h3><?php
    }
    foreach (xcms_all_groups() as $group => $title)
    {
        $attrs = "";
        $belongs = false;
        if ($user and $user->check_rights($group, false))
        {
            $attrs .= " checked=\"checked\" ";
            $belongs = true;
        }
        if ($mode == XDP_READONLY)
            $attrs .= " disabled=\"disabled\" ";
        if ($mode != XDP_COMPACT)
        {
            $g = substr($group, 1);
            echo "<div><input $attrs type=\"checkbox\" name=\"group_$g\" id=\"group_$g-checkbox\" />$title</div>\n";
        }
        elseif ($belongs && ($group != '#all' && $group != '#registered'))
            echo "<span id=\"group_$group\">$group</span> ";
    }
}

function xcmst_draw_user_xsm($user)
{
    global $web_prefix;
    $email = $user->param("email");
    if (xu_empty($email))
        return;
    ?>
    <h3>XSM</h3>
    <div><?php
    $person = xsm_find_person_by_email($email);
    if ($person !== null)
    {
        $person_url = "view-person".xcms_url(array(
            'person_id' => $person['person_id'],
            'school_id' => XSM_SCHOOL_ANK_ID,
        ));
        ?>Карточка участника в XSM:
        <a href="<?php echo "/${web_prefix}xsm/$person_url"; ?>"><?php echo xsm_fi_enc($person); ?></a><?php
    }
    else
    {?>
        По заданному email <tt><?php echo $email; ?></tt> в картотеке XSM ничего не найдено.<?php
    }?>
    </div><?php
}

/**
  * TODO: refactor using sys/controls.php xcmst_control
  **/
function xcmst_input_attrs_from_user($user, $key, $read_only = false, $placeholder = "")
{
    $attrs = "";
    if ($read_only)
        $attrs .= " readonly=\"readonly\" ";
    if ($placeholder)
        $attrs .= " placeholder=\"".htmlspecialchars($placeholder)."\" ";
    echo "class=\"admin-medium\" id=\"$key-input\" name=\"$key\" $attrs value=\"".
        htmlspecialchars($user->param($key))."\"";
}

/**
  * Save page ACL from $_POST request to page info
  **/
function xcms_acl_from_post(&$info)
{
    $edit = "";
    $view = "";

    foreach ($_POST as $key => $value)
    {
        if (substr($key, 0, 5) == "edit_")
            $edit .= " ".substr($key, 5);
        if (substr($key, 0, 5) == "view_")
            $view .= " ".substr($key, 5);
    }
    // lost user-level ACL info here, it is not used as for now
    $info["edit"] = $edit;
    $info["view"] = $view;
}

/**
  * Prints (group) access matrix
  * When @name $info is false, prints default ACL
  **/
function xcmst_print_acl($info = false)
{
    $default = ($info === false);

    if (!$default)
    {
        $edit = $info["edit"];
        $view = $info["view"];

        $edit = explode(EXP_SP, trim($edit));
        $view = explode(EXP_SP, trim($view));
    }

    $all_groups = xcms_all_groups();
?>
<h3>Матрица доступа</h3>
<table class="access-editor">
    <tr>
        <th>Группа</th>
        <th>Чтение</th>
        <th>Запись</th>
    </tr>
<?php
    $checked_attr = 'checked="checked"';
    foreach ($all_groups as $g => $translation)
    {
        if (xu_empty($translation))
            continue;

        $enable_view = "";
        if (!$default && array_search($g, $view) !== false)
            $enable_view = $checked_attr;

        $enable_edit = "";
        if (!$default && array_search($g, $edit) !== false)
            $enable_edit = $checked_attr;

        if ($default && $g == "#all")
            $enable_view = $checked_attr;
        if ($default && $g == "#editor")
            $enable_edit = $checked_attr;
        echo
            "<tr><td>$translation</td>".
            "<td><input type=\"checkbox\" name=\"view_$g\" id=\"view_$g-checkbox\" $enable_view /></td>".
            "<td><input type=\"checkbox\" name=\"edit_$g\" id=\"edit_$g-checkbox\" $enable_edit /></td>".
            "</tr>";
    }
?>
</table><?php
}

?>