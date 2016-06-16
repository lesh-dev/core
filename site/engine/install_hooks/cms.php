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

    /**
      * Собственно процесс установки: создаём начальную страницу сайта, если контент пуст.
      * @return true, если у нас это получилось
      **/
    function install($config, &$logs)
    {
        global $engine_dir;
        global $content_dir;
        // FIXME: refactor cms/pages
        $pages_dir = "${content_dir}cms/pages";
        mkdir($pages_dir, 0777, true);
        $root_info_file_name = xcms_get_info_file_name("");  // root page

        if (!file_exists($root_info_file_name))
        {
            $root_info = array(
                "owner" => "root",
                "type" => "content",
                "header" => "Main page",
                "alias" => "",
                "view" => "#all",
                "edit" => "#all",
            );
            if (!xcms_save_list($root_info_file_name, $root_info))
            {
                return "Cannot save '$root_info_file_name' list. ";
            }
        }
        if (!glob("${content_dir}auth/usr/*.user"))
        {
            $root_usr_filename = "${content_dir}auth/usr/root.user";
            $creation_timestamp = time();
            $root_usr_content =
                "login:root\n".
                "email:root@example.com\n".
                "creator:installer\n".
                "creation_date:$creation_timestamp\n".
                "password:7ac7678d5fca55cdd3ef609360a0e262\n".
                "groups:ank,editor,admin\n";
            if (!xcms_write($root_usr_filename, $root_usr_content))
            {
                return "Cannot save user file '$root_usr_filename'. ";
            }
        }

        return true;
    }
    } // class

    /**
      * Объект необходимо инстанциировать в переменную с названием $hook.
      **/
    $hook = new CMSHook();
