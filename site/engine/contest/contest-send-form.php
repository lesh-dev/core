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
require_once("${engine_dir}sys/db.php");
require_once("${engine_dir}contest/scheme.php");

$show_form = true;
$max_attachment_size = 20 * 1024 * 1024;

//$contest_mail = "contest@fizlesh.ru";
$contest_mail = "fizleshcontest@yandex.ru";
$contest_mail_ht = "<a href=\"mailto:$contest_mail\">$contest_mail</a>";

function ctx_submit_solution()
{
    $timestamp = time();
    $data = $_POST;
    $data["sender"] = @$_SERVER["REMOTE_ADDR"]." (".@$_SERVER["REMOTE_HOST"].")";
    $data["submission_timestamp"] = $timestamp;
    ctx_update_object("submission", $data);

    ?>
    <h3>Спасибо, Ваше решение принято!</h3>
    <p>Мы свяжемся с Вами в течении трёх дней. Если за этот срок
    Вам на почту не придёт уведомления,
    отправьте, пожалуйста, решение еще раз.</p>
    <?php
}

if (@$_POST["send-contest"])
{
    $fileexchange_link = xcms_get_key_or($_POST, "fileexchange");
    $data = $_POST;
    if (xu_not_empty($fileexchange_link))
    {
        // process file exchange link
        ctx_submit_solution();
        $show_form = false;
    }
    else
    {
        $file_name = @$_FILES["attachment"]["name"];
        $tmp_name = @$_FILES["attachment"]["tmp_name"];
        $size = @$_FILES["attachment"]["size"];
        $error = @$_FILES["attachment"]["error"];

        if ($size > $max_attachment_size ||
            $error == UPLOAD_ERR_INI_SIZE ||
            $error == UPLOAD_ERR_FORM_SIZE)
        {
            xcms_log(XLOG_ERROR, "[CONTEST] File too large. Error: $error, size: $size");
            ?>
            <font color="red"><b>Ошибка отправки решения</b>:
                файл слишком большой. Максимальный размер файла:
                <b>15&nbsp;МБ</b></font><?php
        }
        elseif (!strlen($file_name))
        {
            xcms_log(XLOG_ERROR, "[CONTEST] File name not set");
            ?>
            <font color="red"><b>Ошибка отправки решения</b>:
                не выбран файл!</font><?php
        }
        elseif ($error !== 0)
        {
            xcms_log(XLOG_ERROR, "[CONTEST] Unknown file upload error: $error");
            ?>
            <font color="red"><b>Ошибка отправки решения.</b>.
                Попробуйте ещё раз. Если эта ошибка повторяется,
                пожалуйста, отправьте решение на адрес
                <?php echo $contest_mail_ht; ?>.</font><?php
        }
        else
        {
            ctx_submit_solution();
            $show_form = false;
        }
    }
}
if ($show_form) { ?>
<p>
    Решение должно представлять из себя архив <b>размером не более 15~МБ</b>.
    Вложите в архив любые файлы, которые сочтёте нужным~---
    отсканированные тексты, фотографии экспериментальных установок и~т.п.
</p>

<p>
    Если архив получился слишком большим, сделайте несколько архивов так,
    чтобы каждая его часть не превышала 15~МБ. Обязательно приложите к каждой части
    текстовый документ (*.txt, *.doc) со следующей информацией:
    <ul>
        <li>ФИО автора работы</li>
        <li>Город, школа, класс</li>
        <li>Адрес электронной почты</li>
        <li>Количество частей и номер данной части (например, Часть 1 из 3)</li>
    </ul>
</p>
<p>
    Альтернативный способ: воспользуйтесь файлообменными сервисами
    <a href="http://disk.yandex.ru">Яндекс.Диск</a>,
    <a href="http://files.mail.ru">Файлы.MAIL.RU</a>
    или любым другим. Залейте архив с решением на файлообменник, получите ссылку
    на загруженный файл и отправьте её через форму ниже (в этом случае поле
    <b>Архив с решением</b> заполнять не нужно).
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
    <input type="hidden" name="MAX_FILE_SIZE"
        value="<?php echo $max_attachment_size; ?>">
    <table>
        <tr>
            <td>Электронная почта</td>
            <td><input name="mail" id="mail-input" type="text"/></td>
        </tr>
        <tr>
            <td>Ссылка на файлообменник</td>
            <td><input name="fileexchange" id="fileexchange-input" type="text" /></td>
        </tr>
        <tr>
            <td>или</td>
            <td>&nbsp;</td>
        </tr>
        <tr>
            <td>Архив с решением</td>
            <td><input name="attachment" id="attachment-file" type="file"/></td>
        </tr>
    </table>
    <input type="submit" name="send-contest" id="send-contest-submit" value="Отправить" />
</form>

<p>
    Оставьте, пожалуйста, работающий и читаемый Вами адрес
    электронной почты. Мы оповестим Вас о том, что решение получено.
    Если Вы не получите оповещения в течении трёх дней~---
    пошлите решение еще раз.
</p>
<?php } ?>