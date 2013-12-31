<?php
/* User-related middleware */

define('XDP_NORMAL', 1);
define('XDP_READONLY', 2);
define('XDP_COMPACT', 3);

function xcmst_draw_privileges($user, $mode = XDP_NORMAL)
{
    if ($mode != XDP_COMPACT)
    {?>
        <h3>Привилегии</h3><?php
    }
    foreach(xcms_all_groups() as $group => $title)
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
            echo "<div><input $attrs type=\"checkbox\" name=\"group_$group\" id=\"group_$group\" />$title</div>\n";
        elseif ($belongs && ($group != '#all' && $group != '#registered'))
            echo "<span id=\"group_$group\">$group</span> ";
    }
}

/**
  * See also sys/tag.php for xcmst_input_attrs_from_post,
  * it is almost a copy specialized for user
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

function xcmst_print_acl($all_groups, $list, $mode)
{
    $acl = explode(EXP_SP, trim($list[$mode]));
    foreach ($acl as $key=>$value)
    {
        if (!$value)
            continue;

        $t = xcms_get_key_or($all_groups, $value);
        echo "<div><input type=\"checkbox\" name=\"$mode-$value\" checked=\"checked\">$t ($value)<div/>";
    }
    echo "Добавить: <select name=\"add-$mode\" id=\"add-$mode\">";
    echo "<option value=\"\">(не добавлять)</option>";
    foreach ($all_groups as $k=>$v)
    {
        if(!strlen($v)) continue;
        echo "<option value=\"$k\">$v</option>";
    }
    echo "</select></div>";
}

?>