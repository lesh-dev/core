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
    <h1>СТОЙ!!! ПОДУМАЙ, ЧТО ТЫ ДЕЛАЕШЬ!!!!</h1><?php
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
