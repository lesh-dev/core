<?php

function xcmst_contest_delete_entity()
{
    if (@$_POST["delete"])
    {
        xdb_delete(@$_GET["table"], @$_GET["id"]);
        ?><p>Запись удалена успешно</p><?php
        return;
    }
    ?>
    <h3>Запрос на удаление</h3>
    <h2>Стой! Подумай, что ты делаешь!</h2><?php
    $table = @$_GET["table"];
    $id = @$_GET["id"];
    ?>
    <p>Таблица: <?php echo $table; ?></p>
    <p>Идентификатор: <?php echo $id; ?></p>
    <table class="table table-striped table-bordered table-condensed table-hover"><?php

    $record = xdb_get_entity_by_id($table, $id);
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
    $id = $work["contestants_id"];
    $row = "";
    if ($simple)
    {
        $row .= "<td>".$work['name']."</td>";
    }
    else
    {
        $row .=
            "<td><a href=\"/ctx/contestants/view/$id\">{$work["name"]}</a></td>".
            "<td>{$work["level"]}</td>".
            "<td><a href=\"{$work["work"]}\">Скачать</a></td>";

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
        $row .= "<td><a href=\"/ctx/contestants/delete/$id\">Удалить</a></td>";
    }
    return $row;
}

