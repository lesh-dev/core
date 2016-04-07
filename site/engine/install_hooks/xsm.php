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
                "default"=>"ank/fizlesh.sqlite3"
            )
        );
    }
    /**
      * Мы любим считать длины строк, поэтому нам нужен модуль php-mbstring.
      * Проверяем его по наличию функции mb_strlen.
      * Мы также пользуемся sqlite3, поэтому проверяем наличие класса SQlite3.
      * @return true, если все требуемые объекты найдены и сообщение об ошибке
      * в противном случае.
      **/
    function initial_check()
    {
        if (!function_exists('mb_strlen'))
            return "PHP function 'mb_strlen' is missing. Please install php-mbstring package/module. ";

        if (!class_exists('SQlite3'))
            return "PHP class 'SQlite3' is missing. Please install php5-sqlite package/module. ";

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
      * Временный костыль, см. TODO по месту его использования
      **/
    function _init_db_component($config, &$logs, $db_name, $name)
    {
        global $engine_dir;
        $content_dir = $config["content_dir"];
        $log_name = "$content_dir/dbinit-$name.log";
        $db_init = "$engine_dir/dbpatches/dbinit-$name.sql";
        if (system("sqlite3 $db_name < $db_init > $log_name 2>&1") != 0)
        {
            $sqlite_log = @file_get_contents($log_name);
            $logs .= "<pre>".htmlspecialchars($sqlite_log)."</pre>\n";
            return false;
        }
        return true;
    }

    /**
      * Дописываем в settings.php блок метаинформации
      * @return true, если у нас это получилось
      **/
    function install($config, &$logs)
    {
        global $engine_dir;
        $result = xcms_append("settings.php",
            // TODO: привет кавычкам
            "<?php\n/* This block was inserted by installer -- xsm.php.".
            "\nYou may edit it, but it can be regenerated. */".
            "\n    \$SETTINGS['xsm_db_name'] = '".$config["xsm_db_name"]."';".
            "\n/* --- */\n?>");
        if (!$result)
            return "Cannot open 'settings.php' for append. ";

        $content_dir = $config["content_dir"];
        $db_name = $content_dir.$config["xsm_db_name"];
        if (!file_exists($db_name))
        {
            // TODO: move dbinit to separate routine, checking table existance
            $logs .= "<li>[XSM] Creating fresh database <tt>".htmlspecialchars($db_name)."</tt></li>\n";
            @mkdir(dirname($db_name), 0777, true);
            $result = $result && $this->_init_db_component($config, $logs, $db_name, "notify");
            $result = $result && $this->_init_db_component($config, $logs, $db_name, "xsm");
            $result = $result && $this->_init_db_component($config, $logs, $db_name, "contest");
        }
        return $result ? true : "DB initialization failed, see transcript in logs";
    }
    } // class

    /**
      * Объект необходимо инстанциировать в переменную с названием $hook.
      **/
    $hook = new XSMHook();
?>