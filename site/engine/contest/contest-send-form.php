<?php
/**
 * Пожалуйста, не редактируйте этот код в редакторе, исправляйте
 * его прямо в репозитории и копируйте методом Ctrl-C, Ctrl-V на страницу
 * ПОЛНОСТЬЮ. В противном случае очень тяжело следить за изменениями этого кода.
 * Длина строки не должна превышать 80 символов.
 *
 * Файл расположен в site/engine/contest/contest-send-form.php
 * Alias страницы: contest/send
 **/

require_once("${engine_dir}sys/db.php");
require_once("${engine_dir}contest/scheme.php");

if (true)
{?>
    <p>Приём работ олимпиады в электронном виде закрыт.</p><?php
}
else
{

$show_form = true;
$max_attachment_size = 20 * 1024 * 1024;

//$contest_mail = "contest@fizlesh.ru";
$contest_mail = "fizleshcontest@yandex.ru";
$contest_mail_ht = "<a href=\"mailto:$contest_mail\">$contest_mail</a>";

function ctx_notify_three_days()
{
    global $contest_mail_ht;
    ?>
    <p>Мы свяжемся с Вами в течении трёх дней. Если за этот срок
    Вам на почту не придёт уведомления, обязательно свяжитесь
    с нами по электронной почте <?php echo $contest_mail_ht; ?>.</p><?php
}

function ctx_submit_solution()
{
    $timestamp = time();
    $sender = @$_SERVER["REMOTE_ADDR"]." (".@$_SERVER["REMOTE_HOST"].")";
    $data = $_POST;
    $mail = xcms_get_key_or($data, "mail");
    $data["sender"] = $sender;
    $data["submission_timestamp"] = $timestamp;
    ctx_update_object("submission", $data);

    $body_html = xcms_get_html_template("ctx_new_submission");
    $body_html = str_replace('@@MAIL@', htmlspecialchars($mail), $body_html);
    $body_html = str_replace('@@SENDER@', htmlspecialchars($sender), $body_html);
    $body_html = str_replace('@@TIMESTAMP@', htmlspecialchars(xcms_datetime($timestamp)), $body_html);
    xcms_send_notification("ctx", NULL, $body_html);
    ?>
    <h3>Спасибо, Ваше решение принято!</h3><?php
    ctx_notify_three_days();
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
        $attachment = xcms_get_uploaded_file("attachment", $max_attachment_size, 512);
        $exception_code = $attachment["exception_code"];
        if ($exception_code == XE_FILE_TOO_LARGE)
        {?>
            <font color="red"><b>Ошибка отправки решения</b>:
                файл слишком большой. Максимальный размер файла:
                <b>15&nbsp;МБ</b></font><?php
        }
        elseif ($exception_code == XE_FILE_TOO_SMALL)
        {?>
            <font color="red"><b>Ошибка отправки решения</b>:
                не выбран файл (или его размер подозрительно маленький)!</font><?php
        }
        elseif ($exception_code == XE_FILE_UPLOAD_ERROR)
        {?>
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
    <a href="https://disk.yandex.ru">Яндекс.Диск</a>,
    <a href="https://cloud.mail.ru">Облако.MAIL.RU</a>
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

<p>Оставьте, пожалуйста, работающий и читаемый Вами адрес
электронной почты. Мы оповестим Вас о том, что решение получено.</p><?php
ctx_notify_three_days(); ?>
<?php }
} // end if
?>