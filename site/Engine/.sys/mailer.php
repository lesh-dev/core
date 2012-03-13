<?
  function send_notify_mail($target_list,$subject,$mail_text)
  {
    global $SETTINGS;
    $message = $mail_text;
    $message = wordwrap($message, 70);
    $list = getList("{$SETTINGS["datadir"]}cms/mailer.conf");
    $ml = $list[$target_list];
    if(!mail($ml, $subject, $message))
      echo "<li>SENDMAIL FAILED: <li>forTarget: $ml <li>withSubject: $subject <li>withText: <pre>$message</pre>";
  }
?>