<?php
    include_once("$engine_dir/sys/phpmailer/class.phpmailer.php");
    include_once("$engine_dir/sys/util.php");
    include_once("$engine_dir/sys/db.php");

    function xcms_get_mailer($addr_from, $name_from)
    {
        $mailer = new PHPMailer();
        $mailer->CharSet = "utf-8";
        // please note this address should be configured in postfix
        $mailer->SetFrom($addr_from, $name_from);
        $mailer->Sender = $addr_from;
        return $mailer;
    }

    function xcms_mailer_send($mailer, $subject, $body_html)
    {
        $mailer->Subject = $subject;
        // plain text letters is a former century
        $mailer->MsgHTML($body_html);
        $mailer->AltBody = "This message is in HTML format.\r\n";

        if (!$mailer->Send())
        {
            xcms_log(XLOG_ERROR, "[MAILER] ".$mailer->ErrorInfo);
            return false;
        }
        return true;
    }

    define('XMAIL_DESTMODE_TO', 'to');
    define('XMAIL_DESTMODE_CC', 'cc');
    define('XMAIL_DESTMODE_BCC', 'bcc');

    function xcms_get_notification_fields()
    {
        return array(
            "mail_group"=>"Почтовая группа",
            "notification_text"=>"Текст уведомления в формате plain text",
            "notification_html"=>"Текст уведомления в формате HTML"
        );
    }

    /**
      * For internal usage only
      **/
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
        $mails = explode('|', $ml);
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
      * For internal usage only
      * Баги: Знает про fizlesh.ru, вместо того, чтобы брать эти настройки
      * из конфигурационного файла.
      **/
    function xcms_deliver_mail_int($mail_group, $addr_list, $prefix, $notification_body, $subject = '')
    {
        global $SETTINGS;

        if (empty($subject))
            $subject = "Уведомления [$mail_group]";

        $body_html = file_get_contents("{$SETTINGS['engine_dir']}templates/notification-template.html");
        $body_html = str_replace('@@NOTIFICATION-BODY@', $notification_body, $body_html);
        $body_html = str_replace('@@SUBJECT@', $subject, $body_html);

        $addr_from = "noreply@fizlesh.ru"; // TODO: remove these spikes!
        $name_from = "FizLesh Notificator";
        $mailer = xcms_get_mailer($addr_from, $name_from);
        $mailer->AddReplyTo($addr_from, $name_from);

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

        $host = xcms_hostname();
        return xcms_mailer_send($mailer, "[xcms-$prefix] ($host) $subject", $body_html);
    }


    /**
      * Ставит почтовое уведомление в очередь
      * @param mail_group Группа рассылки из списка mailer.conf (или NULL)
      * @param addr_list Список адресов помимо группы рассылки (или NULL).
      *        Если указан одновременно и адрес, и группа рассылки, то письмо отправляется
      *        по указанному адресу, а адресаты из группы рассылки ставятся в BCC.
      * @param prefix Префикс для удобной фильтрации писем: [xcms-<prefix>]
      * @param subject Тема уведомления
      * @param mail_text Тело уведомления (в формате plain text)
      * @param mail_text_html Тело уведомления (в формате html)
      * @param immediate Послать письмо немедленно, не складывая в очередь
      **/
    function xcms_send_notification($mail_group, $addr_list, $prefix, $subject, $mail_text, $mail_text_html, $immediate = false)
    {
        global $SETTINGS;
        $login = xcms_user()->login();
        $enabled = xcms_get_key_or($SETTINGS, "mailer_enabled", true);
        if (!$enabled) return;

        $unix_time = time();
        $hr_timestamp = date("Y.m.d H:i:s", $unix_time);

        $host = xcms_hostname();
        $body_text =
            "$mail_text\r\n".
            "--\r\n".
            "Это уведомление сгенерировано автоматически. Отвечать на него не нужно\r\n".
            "Пользователь    : $login\r\n".
            "Имя хоста       : $host\r\n".
            "Обратная ссылка : {$_SERVER['HTTP_REFERER']}\r\n";
            "Дата и время    : $hr_timestamp\r\n";

        if (!empty($mail_text_html))
        {
            $body_html = file_get_contents("{$SETTINGS['engine_dir']}templates/notification-body.html");
            $body_html = str_replace('@@MESSAGE@', $mail_text_html, $body_html);
            $body_html = str_replace('@@HOST@', $host, $body_html);
            $body_html = str_replace('@@REFERER@', $_SERVER['HTTP_REFERER'], $body_html);
            $body_html = str_replace('@@LOGIN@', $login, $body_html);
            $body_html = str_replace('@@TIMESTAMP@', $hr_timestamp, $body_html);
        }
        if ($immediate)
            return xcms_deliver_mail_int($mail_group, $addr_list, $mail_group, $body_html, $subject);

        // In case of delayed sending, subject and prefix are lost
        $values = array(
            "mail_group"=>$mail_group,
            "notification_text"=>$body_text,
            "notification_html"=>$body_html
        );

        return xdb_insert_or_update("notification", array("notification_id"=>XDB_NEW), $values, xcms_get_notification_fields());
    }

    /**
      * Доставляет накопленные почтовые уведомления
      * Баги: Знает про fizlesh.ru, вместо того, чтобы брать эти настройки
      * из конфигурационного файла.
      * @param mail_group Группа рассылки из списка mailer.conf (или NULL)
      **/
    function xcms_deliver_notifications($mail_group)
    {
        // it is essential to open DB in write mode to lock it
        $db = xdb_get_write();
        $query = "SELECT * FROM notification WHERE mail_group = '$mail_group' ORDER BY notification_id DESC";
        $notification_sel = $db->query($query);
        $notification_body = "";
        while ($notification = $notification_sel->fetchArray(SQLITE3_ASSOC))
            $notification_body .= $notification['notification_html'];

        if (!xcms_deliver_mail_int($mail_group, null, $mail_group, $notification_body))
            return false;

        // purge notifications in case of success
        $del_query = "DELETE FROM notification WHERE mail_group = '$mail_group'";
        $db->query($del_query);

        return true;
    }
?>
