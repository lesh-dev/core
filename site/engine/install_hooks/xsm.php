<?php
    /**
      * Хук настройки XSM
      * Maintainer: mvel@
      **/
    class XSMHook
    {
    /**
      * Определяет название модуля
      **/
    function module_name()
    {
        return "Конфигурация XSM";
    }
    /**
      * Возвращает список переменных,
      * необходимых модулю для функционирования
      **/
    function request_variables()
    {
        $request_uri = str_replace("install.php", "", $_SERVER["REQUEST_URI"]);
        return array(
            "xsm_db_name"=>array(
                "name"=>"Имя файла БД",
                "type"=>"string",
                "default"=>"fizlesh.sqlite3"
                )
        );
    }
    /**
      * Мы любим считать длины строк, поэтому нам нужен модуль php-mbstring
      * @return true, если найдена функция mb_strlen и сообщение об ошибке
      * в противном случае.
      **/
    function initial_check()
    {
        if (!function_exists('mb_strlen'))
            return "PHP function 'mb_strlen' is missing. Please install php-mbstring package/module. ";
        return true;
    }
    /**
      * Проверяем введённые параметры
      * TODO: нужно проверять существование файла БД
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
    function install($config)
    {
        $f = fopen("settings.php", "a+");
        if (!$f)
            return "Cannot open 'settings.php' for append. ";
        // TODO: привет кавычкам
        fputs($f, "\n<?php /* This block was inserted by installer -- xsm.php.");
        fputs($f, "\nYou may edit it, but it can be regenerated. */");
        fputs($f, "\n   \$xsm_db_name = '".$config["xsm_db_name"]."';");
        fputs($f, "\n/* --- */ ?>\n");
        return true;
    }
    } // class

    /**
      * Объект необходимо инстанциировать в переменную с названием $hook.
      **/
    $hook = new XSMHook();
?>