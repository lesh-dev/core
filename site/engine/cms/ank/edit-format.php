<?php

function xsm_is_bottom_field($key)
{
    if (substr($key, strlen($key) - 8) == "_created" ||
        substr($key, strlen($key) - 9) == "_modified")
        return true;
    return false;
}

function xsm_bottom_fields($table_name, $object)
{
    $obj_created = xcms_get_key_or($object, "${table_name}_created");
    $obj_modified = xcms_get_key_or($object, "${table_name}_modified");
    ?><div class="xsm-bottom-fields">
        <b>Дата создания</b>: <?php echo $obj_created;
        if (xu_not_empty($obj_modified))
        {?>.
            <b>Последняя модификация</b>: <?php echo $obj_created;
        }?>
    </div><?php
}

?>