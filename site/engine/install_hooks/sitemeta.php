<?php
    /**
      * Хук настройки метаинформации о сайте (имя сайта и т.п.)
      * Maintainer: mvel@
      * Author: doctor@
      **/
    class MetaInfoHook
    {
    /**
      * Определяет название модуля
      **/
    function module_name()
    {
        return "Общая информация о веб-сайте";
    }
    /**
      * Возвращает список переменных,
      * необходимых модулю для функционирования
      **/
    function request_variables()
    {
        $request_uri = str_replace("install.php", "", $_SERVER["REQUEST_URI"]);
        return array(
            "site_name"=>array(
                "name"=>"Название веб-сайта",
                "type"=>"string",
                "default"=>$_SERVER["HTTP_HOST"]
                ),
            "site_log_path"=>array(
                "name"=>"Путь до log-файлов",
                "type"=>"string",
                "default"=>"/var/log/".$_SERVER["HTTP_HOST"]."/engine.log",
                ),
            "site_url"=>array(
                "name"=>"Адрес веб-сайта",
                "type"=>"string",
                "default"=>"http://{$_SERVER['HTTP_HOST']}$request_uri"
                ),
            "webmaster_mail"=>array(
                "name"=>"Адрес службы техподдержки",
                "type"=>"string",
                "default"=>"support@".$_SERVER["HTTP_HOST"])
        );
    }
    /**
      * Требования этого модуля тривиальны
      * @return true в любом случае
      **/
    function initial_check()
    {
        return true;
    }
    /**
      * Проверяем введённые параметры
      * Пока что оформлена в виде заглушки.
      * TODO: Сделать минимальную проверку вводимой информации
      **/
    function final_check($config)
    {
        return true;
    }
    /**
      * Удаление модуля: подчищать тут нечего, файлов мы не создаём
      * @return true в любом случае
      **/
    function uninstall()
    {
        return true;
    }
    /**
      * Дописываем в settings.php блок метаинформации
      * @return true, если у нас это получилось
      **/
    function install($config, &$logs)
    {
        $result = xcms_append("settings.php",
            "<?php\n/* This block was inserted by installer -- sitemeta.php.".
            "\nYou may edit it, but it can be regenerated. */".
            "\n   \$meta_site_name = '".$config["site_name"]."';".
            "\n   \$meta_site_url = '".$config["site_url"]."';".
            "\n   \$meta_site_log_path = '".$config["site_log_path"]."';".
            "\n   \$meta_site_mail = '".$config["webmaster_mail"]."';".
            "\n/* --- */\n?>");
        if (!$result)
            return "Cannot open 'settings.php' for append. ";
        return true;
    }
    } // class

    /**
      * Объект необходимо инстанциировать в переменную с названием $hook.
      **/
    $hook = new MetaInfoHook();
?>