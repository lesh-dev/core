<?php
function xcms_check_mod_rewrite()
{
    if (function_exists('apache_get_modules'))
    {
        $modules = apache_get_modules();
        return in_array('mod_rewrite', $modules);
    }
    return (getenv('HTTP_MOD_REWRITE') == 'On');
}

function xcms_check_allow_override()
{
    $header_test_url = str_replace("install.php", "header_test/header_test.php", $_SERVER["REQUEST_URI"]);
    $header_test_url = "http://{$_SERVER['HTTP_HOST']}$header_test_url";
    $ch = curl_init($header_test_url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
    curl_setopt($ch, CURLOPT_HEADER, true);
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 5); // enough for connection
    curl_setopt($ch, CURLOPT_TIMEOUT, 10); // enough for receiving
    $response = curl_exec($ch);
    $http_status = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    return ($http_status == 200 && strpos($response, "X-XCMS-HTAccess-Works") !== false);
}


class InstallerInstallHook
{
    /**
      * Имя модуля
      **/
    function module_name()
    {
        return "Основные настройки";
    }
    function request_variables()
    {
        global $SETTINGS;
        $design_list = glob("*design*", GLOB_ONLYDIR);
        if(count($design_list))
            $design = $design_list[0];
        else $design = "design";

        $content_list = glob("*content*", GLOB_ONLYDIR);
        if(count($content_list))
            $content = $content_list[0];
        else $content = "content";

        // set default values for *each* setting
        $SETTINGS["content_dir"] = "$content/";
        $SETTINGS["design_dir"]  = "$design/";
        $SETTINGS["engine_dir"]  = "engine/";
        $SETTINGS["engine_pub"]  = "engine_public/";
        //$SETTINGS["web_prefix"]  = ;
        $SETTINGS["mailer_enabled"] = true;

        $request_uri = str_replace("install.php", "", $_SERVER["REQUEST_URI"]);

        return array(
            "content_dir" =>
                array("name"=>"Содержимое сайта", "default"=>"$content/")
            ,"design_dir" =>
                array("name"=>"Дизайн", "default"=>"$design/")
            ,"engine_dir" =>
                array("name"=>"Движок", "default"=>"engine/")
            ,"engine_pub" =>
                array("name"=>"Публичное содержимое движка", "default"=>"engine_public/")
            ,"web_prefix" =>
                array("name"=>"Префикс", "default"=>substr($request_uri, 1))
            ,"mailer_enabled" =>
                array("name"=>"Использовать ли оповещения по e-mail", "default"=>"true", "type"=>"bool")
        );

    }
    /**
      * Вызывается перед установкой, проверяет,
      * имеет ли смысл её начинать вообще
      **/
    function initial_check()
    {
        if (!xcms_check_mod_rewrite())
            return
            "<p>Apache '<tt>mod_rewrite</tt>' module is not enabled.<br/>".
            "Please enable it in your Apache webserver configuration.</p>";

        if (!xcms_check_allow_override())
            return
                "<p>Apache '<tt>AllowOverride</tt>' directive is not enabled for site root.<br/>".
                "Aliases will not work. Please enable it in your Apache webserver configuration.</p>";

        @mkdir(".prec", 0777);
        $PERM["prec"] = xcms_append(".prec/.htaccess", "deny from all");
        $PERM["htaccess"] = xcms_append(".htaccess", "");
        $PERM["install"] = xcms_append("install.php", "");
        $PERM["settings"] = xcms_append("settings.php", "");

        if(!$PERM["htaccess"])
        {
            return "<p>Script can't write to site root folder. You should do either</p>
            <ul>
                <li>change rights to root folder to make it writeable</li>
                <li>create (writeable) folder .prec and empty writeable .htaccess file</li>
            </ul>";
        }

        if(!$PERM["prec"])
            return "<p>Folder <tt>.prec/</tt> is not writeable. Please fix this problem.</p>";

        if(!$PERM["install"])
            return "<p>File <tt>./install.php</tt> is not writeable. Please fix this problem.</p>";

        if(!$PERM["settings"])
            return "<p>File <tt>./settings.php</tt> is not writeable. Please fix this problem.</p>";

        return true;
    }

    /**
      * Вызывается после того, как пользователь введёт параметры установки
      **/
    function final_check($config)
    {
        $dirs = array(
            "content_dir",
            "design_dir",
            "engine_dir",
            "engine_pub"
        );

        foreach ($dirs as $d)
            if(!is_dir(@$config[$d]))
                return "$d variable is not a directory. ";
        return true;
    }
    /**
      * Подчищает следы использования модуля, в данном случае удаляет
      * файл с настройками
      * TODO: Кажется, это неправильно -- настройки не надо убивать.
      **/
    function uninstall()
    {
        @unlink("settings.php");
        return true;
    }
    /**
      * Собственно процесс установки
      **/
    function install($config)
    {
        global $SETTINGS;
        global $content_dir;
        $dirs = array(
            "content_dir",
            "design_dir",
            "engine_dir",
            "engine_pub"
        );

        $string_settings = array(
            'content_dir',
            'design_dir',
            'engine_dir',
            'engine_pub',
            'web_prefix'
        );
        $bool_settings = array(
            'mailer_enabled'
        );

        $output = "<?php\n";
        foreach ($string_settings as $k)
        {
            $val = $config[$k];
            $val = str_replace('"', '\"', $val);
            $output .= "\x20\x20\x20\x20\$$k = \"$val\";\n";
        }
        foreach($bool_settings as $k)
        {
            $v = $config[$k] ? "true" : "false";
            $output .= "\x20\x20\x20\x20\$$k = $v;\n";
        }
        $output .= "\n?>";
        if (!xcms_append("settings.php", $output))
            return "Cannot append settings to 'settings.php'. ";

        include("settings.php");
        include("${engine_dir}sys/settings.php");
        require_once("${engine_dir}sys/tag.php");
        require_once("${engine_dir}sys/cms.php");
        require_once("${engine_dir}cms/alias.php");
        require_once("${engine_dir}cms/build_rewrite.php");
        xcmst_rebuild_aliases_and_rewrite();

        return true;
    }
} // class InstallerInstallHook

/**
  * Объект необходимо инстанциировать в переменную с названием $hook
  **/
$hook = new InstallerInstallHook();
?>