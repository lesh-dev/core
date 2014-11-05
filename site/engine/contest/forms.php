<?php

function xcmst_draw_contest_form_field($desc, $value, $id)
{
    global $web_prefix;

    $type = $desc["type"];
    $name = $desc["name"];
    $readonly = xcms_get_key_or($desc, "readonly", false);

    $a_readonly = $readonly ? " readonly=\"readonly\" " : "";

    $value = htmlspecialchars($value);
    if ($type == "pk")
    {
        if (!strlen($value))
            $value = XDB_NEW;
        echo "<input type=\"hidden\" name=\"$id\" value=\"$value\" />";
    }
    elseif ($type == "text" || $type == "link" || $type == "timestamp")
    {
        $aux_value = "";
        if ($type == "timestamp")
            $aux_value = xcms_datetime($value);
        echo "<tr>\n".
            "<td>$name</td>\n".
            "<td><input type=\"text\" $a_readonly placeholder=\"$name\" name=\"$id\" id=\"$id-input\" value=\"$value\" /> $aux_value</td>\n".
            "</tr>\n";
    }
    elseif ($type == "file")
    {
        $aux_value = "(нет файла)";
        if (xu_not_empty($value))
            $aux_value = "<a href=\"/$web_prefix$value\">Текущий файл</a>";

        echo "<tr>\n".
            "<td>$name</td>\n".
            "<td><input name=\"$id\" id=\"$id-file\" type=\"file\" value=\"$value\" /> $aux_value</td>\n".
            "</tr>\n";
    }
    elseif ($type == "large")
    {
        echo "<tr><td colspan=\"2\">$name:</td></tr>\n".
            "<tr><td colspan=\"2\">\n".
            "<textarea class=\"field span12\" rows=\"8\" name=\"$id\" id=\"$id-text\">$value</textarea></td>\n".
            "</tr>\n";
    }
    elseif ($type == "checkbox")
    {
        echo "<tr><td>$name</td><td>";
        xcmst_control($id, $value, $name, "", $type);
        echo "</td></tr>\n";
    }
    else
    {
        echo "<tr>\n".
            "<td>$name</td>\n".
            "<td>{{UNKNOWN FIELD of type $type}}</td>\n".
            "</tr>\n";
    }
}

function xcmst_draw_contest_form_view($desc, $value)
{
    global $web_prefix;

    $type = $desc["type"];
    $name = $desc["name"];

    $value = htmlspecialchars($value);
    if ($type == "pk")
    {
        // do not render it
    }
    elseif ($type == "file")
    {
        echo "<tr><th>$name</th><td>";
        if (xu_not_empty($value))
            echo "<a href=\"/$web_prefix$value\">Скачать</a>";
        else
            echo "(нет файла)";
        echo "</td></tr>\n";
    }
    elseif ($type == "text" || $type == "timestamp")
    {
        if ($type == "timestamp")
            $value = xcms_datetime($value);
        echo "<tr><th>$name</th><td>$value</td></tr>\n";
    }
    elseif ($type == "link")
    {
        echo "<tr><th>$name</th><td><a href=\"$value\">$value</a></td></tr>\n";
    }
    elseif ($type == "large")
    {
        if (xu_empty($value))
            $value = "&nbsp;";
        echo "<tr><th colspan=\"2\">$name:</th></tr>\n";
        echo "<tr><td colspan=\"2\">$value</td></tr>\n";
    }
    else
    {
        echo "<tr><th>$name</th><td>{{UNKNOWN FIELD of type $type}}</td></tr>\n";
    }
}
