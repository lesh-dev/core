<?php

function xcmst_contest_delete_entity()
{
    global $ctx_prefix;

    $table_name = xcms_get_key_or($_GET, "table_name");
    if (xu_empty($table_name))
    {?>
        <p>Не указана таблица, Вы куда-то не туда нажали</p><?php
        // TODO: better diagnostics
        return;
    }
    $entry_id = xcms_get_key_or($_GET, "entry_id", XDB_INVALID_ID);
    if (@$_POST["delete"])
    {
        xdb_delete($table_name, $entry_id);
        $redir = "$ctx_prefix/$table_name";
        ?><p>Запись удалена успешно.
            <a href="<?php echo $redir; ?>">Вернуться к списку</p><?php
        return;
    }
    ?>
    <h3>Запрос на удаление</h3>
    <h2>Стой! Подумай, что ты делаешь!</h2><?php
    ?>
    <p>Таблица: <?php echo $table_name; ?></p>
    <p>Идентификатор: <?php echo $entry_id; ?></p>
    <table class="table table-striped table-bordered table-condensed table-hover"><?php

    $record = xdb_get_entity_by_id($table_name, $entry_id);
    foreach ($record as $key=>$value)
    {
        echo "<tr><td>$key</td><td>$value</td></tr>\n";
    }?>
    </table>
    <form method="post">
    <?php xcmst_submit("delete", "Удалить запись окончательно", "Восстановление будет невозможно", "btn btn-danger"); ?>
    </form><?php
}

function ctx_print_result_row($work, $probs, $simple = false)
{
    global $ref;
    global $web_prefix;
    global $ctx_prefix;

    $contestants_id = $work["contestants_id"];
    $view = "$ctx_prefix/contestants/view/$contestants_id";
    $name = xcms_get_key_or($work, "name", "(ФИО не указано)");
    $row = "";
    $stolen_mark = "";

    if ($simple)
    {
        $row .= "<td>$name</td>";

        foreach ($probs as $prob)
        {
            $pid = $prob["problems_id"];
            $mark = (string)$work["p${pid}val"];
            if ($mark === CTX_STOLEN_SOLUTION)
                $stolen_mark = CTX_STOLEN_SOLUTION_HT;
        }
    }
    else
    {
        $level = xcms_get_key_or($work, "level");
        $links_html = array();
        $work_link = xcms_get_key_or($work, "work");
        if (xu_not_empty($work_link))
            $links_html[] = "<a href=\"/$web_prefix$work_link\">Скачать</a>";
        $fileexchange = xcms_get_key_or($work, "fileexchange");
        if (xu_not_empty($fileexchange))
        {
            $links_html[] = "<a href=\"$fileexchange\">Файлообменник</a>";
        }
        $links_html = implode('&nbsp;|&nbsp;', $links_html);

        $row .=
            "<td><a href=\"$view\">$name</a></td>".
            "<td>$level</td>".
            "<td>$links_html</td>";

        foreach ($probs as $prob)
        {
            $pid = $prob["problems_id"];
            $mark = (string)$work["p${pid}val"];
            $cl = "";
            if ($mark === CTX_NO_SOLUTION)
                $mark = CTX_NO_SOLUTION_HT;
            elseif ($mark === CTX_STOLEN_SOLUTION)
                $mark = CTX_STOLEN_SOLUTION_HT;
            elseif ($mark === CTX_NOT_CHECKED)
                $cl = ' class="ctx-not-checked" ';
            elseif (preg_match('/^\d+$/', $mark))
                $cl = ' class="ctx-int-mark" ';
            else
                $cl = ' class="ctx-bad-mark" ';
            $row .= "<td $cl>";
            $row .= $mark;
            $row .= "</td>";
        }
    }
    $sum = @$work["sum"];
    $row .= "<td class=\"sum\">$sum</td>";
    if ($simple)
    {
        $row .= "<td>$stolen_mark</td>";
    }
    else
    {
        $row .= "<td><a href=\"$ctx_prefix/contestants/delete/$contestants_id\">Удалить</a></td>";
    }
    return $row;
}
