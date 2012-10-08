<?php
    /**
      * Install Hook для логгера
      * Maintainer: mvel@
      **/
    class LoggerInstallHook
    {
    /**
      * Определяет название модуля
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
        return array();
    }

    /**
      * Проверяем, удастся ли писать в лог
      * @return true, если лог-файл удалось открыть на добавление
      **/
    function initial_check()
    {
        require_once "engine/sys/logger.php";
        $f = fopen(xcms_log_filename(), "a+");
        if(!$f)
        {
            @fclose($f);
            return "Logger file '".xcms_log_filename()."' is not writeable. ";
        }
        fclose($f);
        return true;
    }
    /**
      * Будет вызвана для проверки после того, как
      * пользователь введет дополнительные параметры.
      * В нашем случае проверять нечего
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
      * Мы никаких новых файлов не создаём, а удалять сами логи
      * не в нашей компетенции
      * @return true, если зачистка успешна, и строка с ошибкой в противном случае
      **/
    function uninstall()
    {
        return true;
    }
    /**
      * СамыйГлавныйМетод. Собственно, именно в нём
      * можно что-нибудь сделать с устанавливаемой системой.
      * В нашем случае тут делать нечего.
      * @param config массив параметров
      **/
    function install($config)
    {
        return true;
    }
    } // class

    /**
      * Объект необходимо инстанциировать в переменную с названием $hook.
      **/
    $hook = new LoggerInstallHook();
?>