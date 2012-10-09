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

    function xcms_send_notification($mail_group, $addr_list, $subject, $mail_text)
    {
        global $SETTINGS, $login;
        $enabled = xcms_get_key_or($SETTINGS, "mailer_enabled", true);
        if (!$enabled) return;
        $message = $mail_text;
        $dom = "@fizlesh.ru"; // TODO: remove fizlesh.ru spike

        $body =
            "$message\r\n".
            "--\r\n".
            "Это уведомление сгенерировано автоматически. Отвечать на него не нужно\r\n".
            "Пользователь    : $login\r\n".
            "Имя хоста       : ".php_uname('n')." \r\n".
            "Обратная ссылка : {$_SERVER['HTTP_REFERER']}\r\n";

        $mailer = xcms_get_mailer();
        $mailer->AddReplyTo("noreply$dom", "FizLesh Notificator");
        $mailer->SetFrom('notify$dom', 'FizLesh Notificator');

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
        $mailer->Body = $body;
        if (!$mailer->Send())
        {
            xcms_log(XLOG_ERROR, "[MAILER] ".$mailer->ErrorInfo);
            return false;
        }
        return true;
    }
?>
