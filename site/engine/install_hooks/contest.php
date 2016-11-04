<?php
    /**
      * Хук настройки Contest
      * Maintainer: mvel@
      **/
    class ContestHook
    {
    /**
      * Определяет название модуля
      **/
    function module_name()
    {
        return "Конфигурация Contest";
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
      * Проверяем настройки, важные для загрузки файлов.
      * @return true, если все константы в ini годные и сообщение об ошибке
      * в противном случае.
      **/
    function initial_check()
    {
        $post_max_size = ini_get('post_max_size');
        $post_max_size_bytes = $this->_return_bytes($post_max_size);
        if ($post_max_size_bytes < 25 * 1024 * 1024)
            return "Please increase '<tt>post_max_size</tt>' in <tt>php.ini</tt>, 25M is a reasonable minimum (current is $post_max_size). ";

        $upload_max_filesize = ini_get('upload_max_filesize');
        $upload_max_filesize_bytes = $this->_return_bytes($upload_max_filesize);
        if ($upload_max_filesize_bytes  < 20 * 1024 * 1024)
            return "Please increase '<tt>upload_max_filesize</tt>' in <tt>php.ini</tt>, 20M is a reasonable minimum. ";

        return true;
    }
    /**
      * Проверяем введённые параметры
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
      * Костыль для перевода размеров в байты
      **/
    function _return_bytes($val)
    {
        $val = trim($val);
        if (!strlen($val))
            return 0;

        $last = strtolower($val[strlen($val) - 1]);
        switch($last)
        {
            // Модификатор 'G' доступен, начиная с PHP 5.1.0
            case 'g':
                $val *= 1024;
            case 'm':
                $val *= 1024;
            case 'k':
                $val *= 1024;
        }
        return $val;
    }

    /**
      * Настроек нет, всегда отдаём true.
      **/
    function install($config, &$logs)
    {
        return true;
    }
    } // class

    /**
      * Объект необходимо инстанциировать в переменную с названием $hook.
      **/
    $hook = new ContestHook();
?>