<?php
    include_once("$engine_dir/sys/phpmailer/class.phpmailer.php");

    function xcms_get_mailer()
    {
        $mailer = new PHPMailer();
        $mailer->CharSet = "utf-8";
        return $mailer;
    }

    define('XMAIL_DESTMODE_TO', 'to');
    define('XMAIL_DESTMODE_CC', 'cc');
    define('XMAIL_DESTMODE_BCC', 'bcc');

    function xcms_add_mail_group($mailer, $mail_group, $mode = XMAIL_DESTMODE_TO)
    {
        global $SETTINGS;
        $mail_groups = xcms_get_list("{$SETTINGS["datadir"]}cms/mailer.conf");
        $ml = xcms_get_key_or($mail_groups, $mail_group);
        if (empty($ml))
        {
            xcms_log(XLOG_ERROR, "[MAILER] Mail group '$mail_group' not found or empty, skipped");
            return false;
        }
        $mails = explode(',', $ml);
        $added_some = false;
        foreach ($mails as $addr)
        {
            $mail_addr = trim($addr);
            if (empty($mail_addr))
                continue;
            if ($mode == XMAIL_DESTMODE_TO)
                $mailer->AddAddress($mail_addr);
            elseif ($mode == XMAIL_DESTMODE_CC)
                $mailer->AddCC($mail_addr);
            elseif ($mode == XMAIL_DESTMODE_BCC)
                $mailer->AddBCC($mail_addr);
            else
            {
                xcms_log(XLOG_ERROR, "[MAILER] Invalid address type mode '$mode', skipped");
                continue;
            }
            $added_some = true;
        }
        if (!$added_some)
            xcms_log(XLOG_ERROR, "[MAILER] Mail group '$mail_group' does not contain any valid emails, skipped");

        return $added_some;
    }

    /**
      * Посылает почтовое уведомление
      * Баги: Знает про fizlesh.ru, вместо того, чтобы брать эти настройки
      * из конфигурационного файла.
      * @param mail_group Группа рассылки из списка mailer.conf (или NULL)
      * @param addr_list Список адресов помимо группы рассылки (или NULL).
      *        Если указан одновременно и адрес, и группа рассылки, то письмо отправляется
      *        по указанному адресу, а адресаты из группы рассылки ставятся в BCC.
      * @param subject Тема уведомления
      * @param mail_text Тело уведомления (в формате plain text)
      * @param mail_text_html Тело уведомления (в формате html)
      **/
    function xcms_send_notification($mail_group, $addr_list, $subject, $mail_text, $mail_text_html = '')
    {
        global $SETTINGS;
        $login = xcms_user()->login();
        $enabled = xcms_get_key_or($SETTINGS, "mailer_enabled", true);
        if (!$enabled) return;
        $unix_time = time();
        $hr_timestamp = date("Y.m.d H:i:s", $unix_time);

        $body =
            "$mail_text\r\n".
            "--\r\n".
            "Это уведомление сгенерировано автоматически. Отвечать на него не нужно\r\n".
            "Пользователь    : $login\r\n".
            "Имя хоста       : {$_SERVER['HTTP_HOST']}\r\n".
            "Обратная ссылка : {$_SERVER['HTTP_REFERER']}\r\n";
            "Дата и время    : $hr_timestamp\r\n";

        if (!empty($mail_text_html))
        {
            $body_html = file_get_contents("{$SETTINGS['engine_dir']}templates/notification-template.html");
            $body_html = str_replace('@@SUBJECT@', htmlspecialchars($subject), $body_html);
            $body_html = str_replace('@@MESSAGE@', $mail_text_html, $body_html);
            $body_html = str_replace('@@HOST@', $_SERVER['HTTP_HOST'], $body_html);
            $body_html = str_replace('@@REFERER@', $_SERVER['HTTP_REFERER'], $body_html);
            $body_html = str_replace('@@LOGIN@', $login, $body_html);
            $body_html = str_replace('@@TIMESTAMP@', $hr_timestamp, $body_html);
        }

        $mailer = xcms_get_mailer();
        // please note this address should be configured in postfix
        $addr_from = "noreply@fizlesh.ru"; // TODO: remove these spikes!
        $name_from = "FizLesh Notificator";
        $mailer->AddReplyTo($addr_from, $name_from);
        $mailer->SetFrom($addr_from, $name_from);
        $mailer->Sender = $addr_from;

        if ($addr_list !== NULL)
        {
            foreach ($addr_list as $mail_addr)
                $mailer->AddAddress($mail_addr);
            // we send an email to address list, but add groups to BCC
            if ($mail_group !== NULL)
                xcms_add_mail_group($mailer, $mail_group, XMAIL_DESTMODE_BCC);
        }
        else
        {
            // regular notification
            if ($mail_group !== NULL)
                xcms_add_mail_group($mailer, $mail_group);
        }
        $mailer->Subject = $subject;
        if (!empty($mail_text_html))
        {
            $mailer->MsgHTML($body_html);
            $mailer->AltBody = $body;
        }
        else
            $mailer->Body = $body;
        if (!$mailer->Send())
        {
            xcms_log(XLOG_ERROR, "[MAILER] ".$mailer->ErrorInfo);
            return false;
        }
        return true;
    }
?>
