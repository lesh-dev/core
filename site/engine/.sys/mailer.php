<?php
    function send_notify_mail($targetList, $subject, $mailText)
    {
        global $SETTINGS, $login;
        if (array_key_exists("mailerEnabled", $SETTINGS) && $SETTINGS["mailerEnabled"] === false) return;
        $message = $mailText;
        $message = wordwrap($message, 160);
        $list = getList("{$SETTINGS["datadir"]}cms/mailer.conf");
        $ml = $list[$targetList];

        $ok = @mail($ml, $subject,
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

        if (!$ok) echo "<li>SENDMAIL FAILED.";
    }
?>