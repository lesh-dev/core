<?php
    /**
      * Пример "инсталл-хука". Вы можете сделать
      * такой же, если Вы хотите контролировать
      * процедуру установки.
      **/
    class LoggerInstallHook
    {
        /**
          * Определяет название модуля
          * и не делает ничего больше
          **/
    function module_name()
    {
        return "Logger Installer Hook";
    }

    /**
      * Возвращает список переменных,
      * необходимых модулю для функционирования
      **/
    function request_variables()
    {
        //return array("another_var"=>array("name"=>"Samble Variable","type"=>"string","default"=>"def"));
        return array();
    }

    /**
      * Эта функция будет вызвана для проверки,
      * удовлетворяет ли система требованиям модуля.
      * @return true, если удовлетворяет, и строку с описанием ошибки, если нет.
      **/
    function initial_check()
    {
        require_once "engine/sys/logger.php";
        $f = fopen(xcms_log_filename(), "a+");
        if(!$f)
        return "Logger file -- ".xcms_log_filename()." -- is not writeable. Fix this.";
        fclose($f);
        return true;
    }
    /**
      * Будет вызвана для проверки после того, как
      * пользователь введет дополнительные параметры.
      * @param config массив параметров
      * @return true, если все в порядке (можно начинать установку)
      * или строку с описанием ошибки, если нельзя.
    **/
    function final_check($config)
    {
        return true;
    }
    /**
      * Эта функция должна полностью подчистить следы использования модуля.
      * Например, если инсталлятор записывает что-то в файл,
      * то этот метод должен файл удалить.
      * @return TODO: описать возвращаемое значение
      **/
    function uninstall()
    {
        return true;
    }
    /**
      * Самый Главный Метод. Собственно, именно в нём
      * можно что-нибудь сделать с устанавливаемой системой.
      * @param config TODO: это массив параметров?
      **/
    function install($config)
    {
        return true;
    }
    }

    /**
      * Объект необходимо инстанциировать в переменную с названием $hook.
      **/
    $hook = new LoggerInstallHook();
?>