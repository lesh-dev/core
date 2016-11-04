<?php
    require_once("${engine_dir}sys/phpmailer/class.phpmailer.php");
    require_once("${engine_dir}sys/template.php");
    require_once("${engine_dir}sys/file.php");
    require_once("${engine_dir}sys/util.php");
    require_once("${engine_dir}sys/tag.php");
    require_once("${engine_dir}sys/db.php");

    function xcms_get_mailer($addr_from, $name_from)
    {
        $mailer = new PHPMailer();
        $mailer->CharSet = "utf-8";
        $mailer->Encoding = "quoted-printable";
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
    define('XMAIL_IMMEDIATE', true);
    define('XMAIL_DEFERRED', false);

    function xcms_get_notification_fields()
    {
        return array(
            "mail_group" => "Почтовая группа",
            "notification_text" => "Текст уведомления в формате plain text",
            "notification_html" => "Текст уведомления в формате HTML",
        );
    }

    /**
      * Checks whether mailer is enabled in configuration
      **/
    function xcms_mailer_enabled()
    {
        // TODO(mvel): Move this setting from SETIINGS to registry?
        global $SETTINGS;
        return xcms_get_key_or($SETTINGS, "mailer_enabled", true);
    }

    /**
      * Obtains mailer configuration file path
      **/
    function xcms_get_mailer_conf_path()
    {
        global $content_dir;
        return "${content_dir}cms/mailer.conf";
    }

    /**
      * Obtains mailer configuration from config file
      **/
    function xcms_get_mailer_conf()
    {
        return xcms_get_list(xcms_get_mailer_conf_path());
    }

    /**
      * For internal usage only
      **/
    function xcms_add_mail_group($mailer, $mail_group, $mode = XMAIL_DESTMODE_TO)
    {
        $mail_groups = xcms_get_mailer_conf();
        $ml = xcms_get_key_or($mail_groups, $mail_group);
        if (xu_empty($ml))
        {
            xcms_log(XLOG_ERROR, "[MAILER] Mail group '$mail_group' not found or empty, skipped");
            return false;
        }
        $mails = explode(EXP_PIPE, $ml);
        $added_some = false;
        foreach ($mails as $addr)
        {
            $mail_addr = trim($addr);
            if (xu_empty($mail_addr))
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
    function xcms_deliver_mail_int($mail_group, $addr_list, $notification_body, $subject = NULL)
    {
        if (!xcms_mailer_enabled()) // disabled mailer should produce no errors
            return true;

        $notification_date = xcms_rus_date();

        if ($subject === NULL)
            $subject = "Уведомления за $notification_date";

        $body_html = xcms_get_html_template("notification-template");
        $body_html = str_replace('@@NOTIFICATION-BODY@', $notification_body, $body_html);
        $body_html = str_replace('@@SUBJECT@', $subject, $body_html);

        $addr_from = "noreply@fizlesh.ru"; // TODO: remove these spikes!
        $name_from = "FizLesh Notificator";
        $mailer = xcms_get_mailer($addr_from, $name_from);
        $mailer->AddReplyTo($addr_from, $name_from);

        $group_mode = XMAIL_DESTMODE_TO;
        if ($addr_list !== NULL)
        {
            foreach ($addr_list as $mail_addr)
                $mailer->AddAddress($mail_addr);
            // we send an email to address list, but add groups to BCC
            $group_mode = XMAIL_DESTMODE_BCC;
        }
        if ($mail_group !== NULL)
        {
            xcms_add_mail_group($mailer, $mail_group, $group_mode);
            $host = xcms_hostname();
            // See bug #798
            $subject = "[$mail_group] ($host) $subject";
        }
        return xcms_mailer_send($mailer, $subject, $body_html);
    }


    /**
      * Ставит почтовое уведомление в очередь
      * @param mail_group Группа рассылки из списка mailer.conf (или NULL),
      *        она же префикс в теме.
      * @param addr_list Список адресов помимо группы рассылки (или NULL).
      *        Если указан одновременно и адрес, и группа рассылки, то письмо отправляется
      *        по указанному адресу, а адресаты из группы рассылки ставятся в BCC.
      * @param mail_text_html Тело уведомления (в формате html)
      * @param subject Тема уведомления (не имеет смысла в случае отложенной отправки)
      * @param immediate Если значение равно XMAIL_IMMEDIATE, письмо будет послано немедленно.
      *        По умолчанию равно XMAIL_DEFERRED, и письмо складывается в очередь для отправки.
      * @param mail_text Тело уведомления (в формате plain text), есть подозрения, что оно
      *        никогда не будет использоваться
      **/
    function xcms_send_notification($mail_group, $addr_list, $mail_text_html, $subject = NULL, $immediate = XMAIL_DEFERRED, $mail_text = NULL)
    {
        if (!xcms_mailer_enabled()) // disabled mailer should produce no errors
            return true;

        $login = xcms_user()->login();
        $real_name = xcms_user()->param("name");
        $hr_timestamp = xcms_datetime();
        $host = xcms_hostname();
        $referer = xcms_get_key_or($_SERVER, "HTTP_REFERER"); // can be empty, see #924
        $body_text =
            "$mail_text\r\n".
            "--\r\n".
            "Это уведомление сгенерировано автоматически. Отвечать на него не нужно\r\n".
            "Пользователь    : $login ($real_name)\r\n".
            "Имя хоста       : $host\r\n".
            "Обратная ссылка : $referer\r\n";
            "Дата и время    : $hr_timestamp\r\n";

        $body_html = "";
        if (xu_not_empty($mail_text_html))
        {
            $body_html = xcms_prepare_html_template("notification-body");
            $body_html = str_replace('@@MESSAGE@', $mail_text_html, $body_html);
            $body_html = str_replace('@@HOST@', $host, $body_html);
            $body_html = str_replace('@@REFERER@', htmlspecialchars($referer), $body_html);
            $body_html = str_replace('@@TIMESTAMP@', $hr_timestamp, $body_html);
        }
        if ($immediate)
            return xcms_deliver_mail_int($mail_group, $addr_list, $body_html, $subject);

        // In case of delayed sending, subject will be lost
        $values = array(
            "mail_group" => $mail_group,
            "notification_text" => $body_text,
            "notification_html" => $body_html,
        );

        return xdb_insert_or_update("notification", array("notification_id" => XDB_NEW), $values, xcms_get_notification_fields());
    }

    /**
      * Доставляет накопленные почтовые уведомления
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
        if (xu_empty($notification_body)) // nothing was added
            return true;

        if (!xcms_deliver_mail_int($mail_group, null, $notification_body))
            return false;

        // purge notifications in case of success
        $del_query = "DELETE FROM notification WHERE mail_group = '$mail_group'";
        $db->query($del_query);

        return true;
    }
