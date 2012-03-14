<?
  function send_notify_mail($target_list,$subject,$mail_text)
  {
    global $SETTINGS,$login;
    $message = $mail_text;
    $message = wordwrap($message, 160);
    $list = getList("{$SETTINGS["datadir"]}cms/mailer.conf");
    $ml = $list[$target_list];
    if(!  $ok= @mail($ml, $subject,
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
    ))
      echo "<li>SENDMAIL FAILED: <li>forTarget: $ml <li>withSubject: $subject <li>withText: <pre>$message</pre>";
  }
?>