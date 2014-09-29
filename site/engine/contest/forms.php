<?php

function xcmst_draw_contest_form_field($type, $name, $value, $id)
{
    $value = htmlspecialchars($value);
    if ($type == "pk")
    {
        if (!strlen($value))
            $value = XDB_NEW;
        echo "<input type=\"hidden\" name=\"$id\" value=\"$value\" />";
    }
    if ($type == "text")
    {
        echo "<tr>\n".
            "<td>$name</td>\n".
            "<td><input type=\"text\" placeholder=\"$name\" name=\"$id\" id=\"$id-input\" value=\"$value\" /></td>\n".
            "</tr>\n";
    }
    if ($type == "file")
    {
        echo "<tr>\n".
            "<td>$name</td>\n".
            "<td><input name=\"$id\" id=\"$id-file\" type=\"file\" value=\"$value\" /></td>\n".
            "</tr>\n";
    }
    if ($type == "large")
    {
        echo "<tr><td colspan=\"2\">$name:</td></tr>\n".
            "<tr><td colspan=\"2\">\n".
            "<textarea class=\"field span12\" rows=\"8\" name=\"$id\" id=\"$id-text\">$value</textarea></td>\n".
            "</tr>\n";
    }
}

function xcmst_draw_contest_form_view($type, $name, $value)
{
    global $web_prefix;
    $value = htmlspecialchars($value);
    if ($type == "pk")
    {

    }
    elseif ($type == "file")
    {
        echo "<tr><th>$name</th><td>";
        if (xu_not_empty($value))
            echo "<a class=\"btn btn-success\" href=\"/$web_prefix$value\">Скачать</a>";
        else
            echo "(нет файла)";
        echo "</td></tr>\n";
    }
    elseif ($type == "text")
    {
        echo "<tr><th>$name</th><td>$value</td></tr>\n";
    }
    elseif ($type == "large")
    {
        if (xu_empty($value))
            $value = "&nbsp;";
        echo "<tr><th colspan=\"2\">$name:</th></tr>\n";
        echo "<tr><td colspan=\"2\">$value</td></tr>\n";
    }
}
