<?php

require_once("${xengine_dir}sys/template.php");

function xcms_console_create_user($params)
{
    $su = xcms_user();
    $su->set_superuser();

    $login = xcms_get_key_or($params, "login");
    $password = xcms_get_key_or($params, "password");
    $email = xcms_get_key_or($params, "email");
    $name = xcms_get_key_or($params, "name");

    $groups = explode(EXP_COM, xcms_get_key_or($params, "groups"));
    $notify = xcms_is_enabled_key($params, "notify", true);

    $su->create($login, $email);
    foreach ($groups as $group)
        $su->add_to_group($login, $group);
    $u = $su->su($login);
    $u->passwd($password);
    $u->set_param("name", $name);

    if ($notify)
    {
        $res = xcms_user_create_notify($email, $login, $password, $name);
        if ($res)
        {
            echo "Cannot send notification to user, do it yourself:\n".
                "EMail: $email, login: $login, password: $password\n";
        }
    }
}

function xcms_user_create_notify($email, $login, $password, $name)
{
    global $meta_site_name;
    return xcms_user_operation_notify("new_user", $email, $login, $password, $name, "Добро пожаловать на $meta_site_name");
}

function xcms_user_password_reset_notify($email, $login, $password, $name)
{
    global $meta_site_name;
    return xcms_user_operation_notify("password_reset", $email, $login, $password, $name, "Выполнен сброс пароля на $meta_site_name");
}

function xcms_user_operation_notify($template_name, $email, $login, $password, $name, $subject)
{
    global $meta_site_name, $meta_site_url, $meta_site_mail;

    $body_html = xcms_get_html_template($template_name);
    $body_html = str_replace('@@SITE@', htmlspecialchars($meta_site_name), $body_html);
    $body_html = str_replace('@@SITE-URL@', htmlspecialchars($meta_site_url), $body_html);
    $body_html = str_replace('@@LOGIN@', $login, $body_html);
    $body_html = str_replace('@@REAL-NAME@', $name, $body_html);
    $body_html = str_replace('@@SUPPORT@', $meta_site_mail, $body_html);

    // do not send private data to [user-change] subscribers
    $body_html_user = str_replace('@@PASSWORD@', htmlspecialchars($password), $body_html);
    $body_html_notify = str_replace('@@PASSWORD@', '***', $body_html);

    $notify_result = xcms_deliver_mail_int(NULL, array($email), $body_html_user, $subject);

    // ignore result here, this is not so important
    xcms_send_notification("user-change", NULL, $body_html_notify, "$subject [admin-bcc]", XMAIL_IMMEDIATE);

    return $notify_result ? null : "Не удалось послать оповещение пользователю. ";
}
