<?php

function xcmst_draw_contest_form_field($type, $name, $value, $id)
{
    if ($type == "pk")
    {
        if (!strlen($value))
            $value = XDB_NEW;
        echo "<input type='hidden' name='$id' value='$value' />";
    }
    if ($type == "text")
    {
        echo "<tr><td class='font-wieght: bold;'>$name</td>
            <td><input type='text' placeholder='$name' name='$id' value='{$value}'/></td></tr>\n";
    }
    if ($type == "file")
    {
        echo "<tr><td>$name</td>
            <td><input name='$id' type=\"file\" value=\"$value\"/></td></tr>\n";
    }
    if ($type == "large")
    {
        echo "<tr><td colspan='2'>$name:</td>
            <tr><td colspan='2'>
                <textarea class='field span12' rows='10' name='$id'>$value</textarea></td></tr>\n";
    }
}

function xcmst_draw_contest_form_view($type, $name, $value)
{
    global $web_prefix;
    if ($type == "pk")
    {

    }
    if ($type == "file")
    {
        echo "<tr><th>$name</th><td><a class='btn btn-success' href='/$web_prefix$value'>Скачать</a></td></tr>\n";
    }
    if ($type == "text")
    {
        echo "<tr><th>$name</th><td>$value</td></tr>\n";
    }
    if ($type == "large")
    {
        echo "<tr><th colspan=2>$name:</th></tr>";
        echo "<tr><td colspan=2>$value</td></tr>\n";
    }
}
