<?php
    include_once("$engine_dir/sys/phpmailer/class.phpmailer.php");

    function xcms_get_mailer()
    {
        $mailer = new PHPMailer();
        $mailer->CharSet = "utf-8";
        return $mailer;
    }

    function xcms_add_mail_group($mailer, $mail_group)
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
            $mailer->AddAddress($mail_addr);
            $added_some = true;
        }
        if (!$added_some)
            xcms_log(XLOG_ERROR, "[MAILER] Mail group '$mail_group' does not contain any valid emails, skipped");

        return $added_some;
    }

    function xcms_send_notification($mail_group, $subject, $mail_text)
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
        xcms_add_mail_group($mailer, $mail_group);
        $mailer->Subject = $subject;
        $mailer->Body = $body;
        if (!$mailer->Send())
        {
            xcms_log(XLOG_ERROR, "[MAILER] ".$mailer->ErrorInfo);
            return false;
        }
        return true;
    }


    /// Это -- последствия "быстрого" разрешения конфликта
    //TODO: написать обертку к новому xmcs_send_notification
    function xcms_send_email($emailList, $subject, $mailText)
    {
        global $SETTINGS, $login;
        if (array_key_exists("mailer_enabled", $SETTINGS) && $SETTINGS["mailer_enabled"] === false) return;
        $message = $mailText;
        $message = wordwrap($message, 160);
        $ok = @mail($emailList, $subject,
            "$message"."\r\n".
            "-- \n".
            "Исполнитель     : $login\n".
            "Имя хоста       : ".php_uname('n')." \n".
            "Обратная ссылка : {$_SERVER['HTTP_REFERER']}\n".
            ""
            ,
            "From: xcms [".php_uname('n')."] mailer  <noreply@fizlesh.ru>\r\n".
            'Content-Type: text/plain; charset=utf-8'."\r\n".
            "Content-Transfer-Encoding: 8bit\r\n"
        );
        return $ok;
    }


?>
