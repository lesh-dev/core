<?
  function send_notify_mail($target_list,$subject,$mail_text)
  {
    global $SETTINGS;
    $message = $mail_text;
    $message = wordwrap($message, 70);
    $list = getList("{$SETTINGS["datadir"]}cms/mailer.conf");
    $ml = $list[$target_list];
    if(!  $ok= @mail($ml, $subject,
        "$message"."\r\n",
        "From: xcms [".php_uname('n')."] mailer  <noreply@fizlesh.ru>\r\n".
        'Content-Type: text/plain; charset=utf-8'."\r\n".
        "Content-Transfer-Encoding: 8bit\r\n"
    ))
      echo "<li>SENDMAIL FAILED: <li>forTarget: $ml <li>withSubject: $subject <li>withText: <pre>$message</pre>";
  }
?>