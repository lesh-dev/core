#!/usr/bin/php
<?php
    function main($args)
    {
        global $cnf,$meta_site_name, $meta_site_url, $meta_site_mail;
        // var_dump(STDIN);
        $command = $args[0];
        if($command == "useradd")
        {
            $su = xcms_user();
            $su->setSuperuser();
            
            $login = @$cnf["login"];
            $password = @$cnf["password"];
            $mail = @$cnf["mail"];
            $groups = @$cnf["groups"];
            $notify = @$cnf["notify"];
            
            if($login == "") throw new Exception("No login specified");
            if($password == "") throw new Exception("No password specified");
            if($mail == "") throw new Exception("No mail specified");
            if($groups == "") throw new Exception("No groups specified");
            if($notify == "yes") $notify = TRUE;
            else if($notify == "yes") $notify = TRUE;
            else throw new Exception("Notify should be 'yes' or 'no'.");
            
            $su->create($login, $mail);
            foreach(explode(",",$groups) as $group)
                $su->groupadd($login, $group);
            $su->su($login)->passwd($password);
            
            $Subj = "Твой логин на сайте $meta_site_name.";
            $Body =
"Привет!

Мы создали для тебя логин и пароль на сайте $meta_site_name ($meta_site_url). Вот они:

Логин (имя пользователя):  $login
Пароль:                    $password

Для того, чтобы войти на сайт, ты можешь пройти по этой ссылке: $meta_site_url

Для того, чтобы редактировать тексты (и добавлять новости), зайди сюда: $meta_site_url?ref=ladmin

Для того, чотбы посмотреть все курсы, зайди сюда: $meta_site_url/register/view-course

Для того, чтобы посмотреть список людей, зайди сюда: $meta_site_url/register/view

Если что-то не так, пароль не подходит, сайт не открывается и т.п. -- пожалуйста, напиши нам на $meta_site_mail

Удачи!
";
            if($notify)
                if(!xcms_send_email($mail, $Subj , $Body))
                {
                    echo "\n *** ERROR. Notification mail could not be delivered. Please, deliver it by yourself.\n";
                    echo "============================================================================\n";
                    echo "To: $mail\n";
                    echo "Sublect: $Subj\n\n";
                    echo $Body;
                    echo "============================================================================\n";
                }
            
        }
    }
?><?php
    $cnf["basedir"] = ".";
    $args = array();
    foreach( $_SERVER["argv"] as $i=>$cmd)
    {
        if($i == 0) continue;
        if(strpos($cmd,"=") !== FALSE)
        {
            $arr = explode("=",$cmd,2);
            $cnf[$arr[0]] = $arr[1];
        }
        else
            $args[] = $cmd;
    }
    $basedir = $cnf["basedir"];
    if(!chdir($basedir))
        throw new Exception("Can't CD to basedir");
    if (!file_exists("index.php"))
        throw new Exception("No index.php found!");
    if (file_exists("install.php"))
        throw new Exception("install.php found, this is uninstalled version!");
    if (!file_exists("settings.php"))
        throw new Exception("setting.php NOT found, this is uninstalled version!");
    
    session_start();
    header("Content-Type: text/html; charset=utf-8");
    date_default_timezone_set('Europe/Moscow');
    require_once ("settings.php");
    require_once ("$engine_dir/sys/settings.php");
    require_once ("$engine_dir/sys/tag.php");
    require_once ("$engine_dir/sys/auth.php");
    require_once ("$engine_dir/sys/logger.php");
    require_once ("$engine_dir/sys/compiler.php");
    require_once ("$engine_dir/sys/mailer.php");
    require_once ("$engine_dir/sys/resample.php");

    $main_ref_file = "";
    $main_ref_name = "";
    xcms_main();
    compile($main_ref_file, $main_ref_name);
    main($args);
?>
