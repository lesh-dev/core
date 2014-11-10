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
        <input name="delete" value="Удалить запись окончательно" class="btn btn-danger" type="submit" />
    </form><?php
}

function ctx_print_result_row($work, $probs, $simple = false)
{
    global $ref;
    global $web_prefix;
    global $ctx_prefix;

    $contestants_id = $work["contestants_id"];
    $view = "$ctx_prefix/contestants/view/$contestants_id";
    $row = "";
    if ($simple)
    {
        $row .= "<td>".$work['name']."</td>";
    }
    else
    {
        $name = xcms_get_key_or($work, "name", "(ФИО не указано)");
        $row .=
            "<td><a href=\"$view\">$name</a></td>".
            "<td>{$work["level"]}</td>".
            "<td><a href=\"/$web_prefix{$work["work"]}\">Скачать</a></td>";

        foreach ($probs as $prob)
        {
            $pid = $prob["problems_id"];
            $row .= "<td>";
            $mark = $work["p${pid}val"];
            $row .= $mark;
            $row .= "</td>";
        }
    }
    $sum = @$work["sum"];
    $row .= "<td class=\"sum\">$sum</td>";

    if (!$simple)
    {
        $row .= "<td><a href=\"$ctx_prefix/contestants/delete/$contestants_id\">Удалить</a></td>";
    }
    return $row;
}
