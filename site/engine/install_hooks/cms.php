<?php
    /**
      * Хук настройки CMS.
      * Написан по мотивам преднастройки пустого сайта.
      * Maintainer: mvel@
      **/
    class CMSHook
    {
    /**
      * Определяет название модуля
      **/
    function module_name()
    {
        return "Конфигурация CMS";
    }
    /**
      * Возвращает список переменных,
      * необходимых модулю для функционирования.
      * В данном случае, всё уже преднастроено базовым модулем.
      **/
    function request_variables()
    {
        return array();
    }
    /**
      * Пре-реквизитов у нас особо нет.
      * @return true
      **/
    function initial_check()
    {
        return true;
    }
    /**
      * Проверяем введённые параметры
      * Параметров у нас нет, праздник никто не портит.
      **/
    function final_check($config)
    {
        return true;
    }
    /**
      * Удаление модуля: подчищать тут нечего, файлов мы не создаём
      * @return true
      **/
    function uninstall()
    {
        return true;
    }

    function _create_page($name)
    {
        global $content_dir;
        // FIXME: refactor cms/pages
        $info_file_name = xcms_get_info_file_name($name);
        $page_dir = "${content_dir}cms/pages/$name";
        @mkdir($page_dir, 0777, true);
        if (!file_exists($info_file_name))
        {
            $page_info = array(
                "owner" => "root",
                "type" => "content",
                "header" => "Root",
                "alias" => "",
                "view" => "#all",
                "edit" => "#all",
            );
            if (!xcms_save_list($info_file_name, $page_info))
            {
                return "Cannot save '$info_file_name' list. ";
            }
        }

        return true;
    }

    /**
      * Собственно процесс установки: создаём начальную страницу сайта, если контент пуст.
      * @return true, если у нас это получилось
      **/
    function install($config, &$logs)
    {
        $result = $this->_create_page("");
        if ($result !== true)
            return $result;
        return $this->_create_page("index");
    }
    } // class

    /**
      * Объект необходимо инстанциировать в переменную с названием $hook.
      **/
    $hook = new CMSHook();
