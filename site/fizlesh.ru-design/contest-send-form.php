<!-- Приём работ олимпиады в электронном виде закрыт. -->
<?php
/**
 * Пожалуйста, не редактируйте этот код в редакторе, исправляйте
 * его прямо в репозитории и копируйте методом Ctrl-C, Ctrl-V на страницу
 * ПОЛНОСТЬЮ. В противном случае очень тяжело следить за изменениями этого кода.
 * Длина строки не должна превышать 80 символов.
 *
 * Файл расположен в fizlesh.ru-design/contest-send-form.php
 * Alias страницы: contest/send
 **/
$need_send = false;
if(@$_POST["send-contest"])
{
    $file_name = @$_FILES["solution"]["name"];
    $tmp_name = @$_FILES["solution"]["tmp_name"];
    $size = @$_FILES["solution"]["size"];
    $error = @$_FILES["solution"]["error"];
    if ($size > 6000000)
        echo "<font color=\"red\">Ошибка отправки решения:
            файл слишком большой</font>";
    else if ($file_name == "")
        echo "<font color=\"red\">Ошибка отправки решения:
            не выбран файл</font>";
    else if ($error !== 0)
        echo "<font color=\"red\">Ошибка отправки решения.</font>";
    else
    {
        @mkdir("$content_dir/contest/");
        $folder = "$content_dir/contest/".time();
        mkdir("$folder");
        $error = false;
        if(!copy($tmp_name, "$folder/$file_name"))
            $error = true;

        $data = array(
            "sender" => @$_SERVER["REMOTE_ADDR"]." (".@$_SERVER["REMOTE_HOST"].")",
            "date" => time(),
            "attachment" => $file_name,
            "mail" => $_POST["mail"]
        );
        xcms_save_list("$folder/config.ini", $data);

        if ($error)
            echo "<font color=\"red\">Ошибка отправки решения.</font>";
        else
        {
            $need_send = true;
            ?>
            <h3>Спасибо, Ваше решение принято!</h3>
            Мы свяжемся с Вами в течении трёх дней. Если за этот срок Вам на почту
            не придёт уведомления,
            отправьте, пожалуйста, решение еще раз
            <?php
        }
    }
}
if (!$need_send) { ?>
<p>
    Решение должно представлять из себя архив не более чем 5~МБ.
    Вложите в архив любые файлы, которые сочтёте нужным~---
    отсканированные тексты, фотографии экспериментальных установок и~т.п.
</p>

<p>
    Большая просьба: пишите разборчиво, крупно и ярко выделяйте номера задач.
</p>

<p>
    Каким бы способом Вы ни оформляли работу, лучше всего отослать её
    на проверку по электронной почте или через сайт. Если Вы оформляете
    ее на бумаге, отсканируйте или сфотографируйте работу (пожалуйста,
    для обеспечения читаемости, не пользуйтесь для этого камерами
    на телефонах).
</p>

<h3>Отправить решение</h3>
<form enctype="multipart/form-data" method="post">
    <input type="hidden" name="MAX_FILE_SIZE" value="6000000">
    <table>
        <tr>
            <td>Архив с решением:</td>
            <td><input name="solution" type="file"/></td>
        </tr>
        <tr>
            <td>Электронная почта:</td>
            <td><input name="mail" type="text"/></td>
        </tr>
    </table>
    <input type="submit" name="send-contest" value="Отправить" />
</form>

<p>
    Оставьте, пожалуйста, работающий и читаемый Вами адрес
    электронной почты. Мы оповестим Вас о том, что решение получено.
    Если Вы не получите оповещения в течении трёх дней~---
    пошлите решение еще раз.
</p>
<?php } ?>