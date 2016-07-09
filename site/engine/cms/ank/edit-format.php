<?php

function xsm_is_bottom_field($key)
{
    if (substr($key, strlen($key) - 8) == "_created" ||
        substr($key, strlen($key) - 9) == "_modified" ||
        substr($key, strlen($key) - 8) == "_deleted")
        return true;
    return false;
}

function xsm_bottom_fields($table_name, $object)
{
    $obj_created = xcms_get_key_or($object, "${table_name}_created");
    $obj_modified = xcms_get_key_or($object, "${table_name}_modified");
    if (xu_not_empty($obj_created))
    {?>
        <div class="xsm-bottom-fields">
            <b>Дата создания</b>: <?php echo $obj_created;
        if (xu_not_empty($obj_modified))
        {?>.
            <b>Последняя модификация</b>: <?php echo $obj_modified;
        }?>
        </div><?php
    }
}

// FIXME: replace with xcmst_hidden common control
function xsm_draw_field_hidden($name, $value)
{
    ?><input
        type="hidden"
        name="<?php echo $name; ?>"
        value="<?php echo $value; ?>"
    /><?php
}

/**
  * Field label
  * @param desc field descriptor
  **/
function xsm_draw_field_label($desc)
{?>
    <span class="ankEditField xsm-label"><?php echo $desc["name"];
    if (xcms_get_key_or($desc, "required"))
        echo "&nbsp;<span class=\"xsm-required-field\">*</span>";
    ?></span><?php
}

function xsm_draw_field_textarea($key, $desc, $value)
{
    ?><textarea
        class="ankEdit"
        name="<?php echo $key; ?>"
        id="<?php echo $key; ?>-text"
        placeholder="<?php echo xcms_get_key_or_enc($desc, "name"); ?>"
        ><?php
        echo htmlspecialchars($value);
    ?></textarea><?php
}

function xsm_draw_field_input($key, $desc, $value)
{
    $attr = xcms_get_key_or($desc, "readonly") ? ' readonly="readonly" ' : '';
    ?><input
        type="text"
        class="ankEdit"
        value="<?php echo htmlspecialchars($value); ?>"
        name="<?php echo $key; ?>"
        id="<?php echo $key; ?>-input"
        placeholder="<?php echo $desc["name"]; ?>"
        <?php echo $attr; ?>
        /><?php
}

/**
  * Typicaly for readonly fields
  **/
function xsm_draw_field_unnamed_input($desc, $value)
{
    $attr = xcms_get_key_or($desc, "readonly") ? ' readonly="readonly" ' : '';
    ?><input
        type="text"
        class="ankEdit"
        value="<?php echo htmlspecialchars($value); ?>"
        <?php echo $attr; ?> /><?php
}

/**
  * @return true when field is processed, false otherwise
  **/
function xsm_draw_generic_fields_begin($desc, $object, $key)
{
    if (xsm_is_bottom_field($key))
        return true;

    $value = xcms_get_key_or($object, $key);

    ?><tr><td class="ankList"><?php

    xsm_draw_field_label($desc);
    $ft = xcms_get_key_or($desc, "type");
    $processed = true;
    if ($ft == "textarea")
        xsm_draw_field_textarea($key, $desc, $value);
    elseif ($ft == "checkbox")
        xsm_checkbox($key, $value);
    elseif ($ft == "enum")
        echo xsm_make_enum_by_type($key, $value, $key);
    elseif ($ft == "input")
        xsm_draw_field_input($key, $desc, $value);
    else
        $processed = false;
    // close processed row
    if ($processed)
    {?>
        </td></tr><?php
    }
    return $processed;
}

function xsm_draw_generic_fields_end()
{
    ?></td></tr><?php
}
