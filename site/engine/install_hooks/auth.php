<?php
    /**
      * InstallHook для модуля авторизации
      * Maintainer: doctor@
      **/
    class AuthInstallHook
    {
    /**
      * Определяет название модуля
      **/
    function module_name()
    {
        return "Пользователи, права и доступ";
    }
    /**
      * Возвращает список переменных,
      * необходимых модулю для функционирования
      **/
    function request_variables()
    {
        return array(
            "superuser_name" =>
                array("name"=>"Имя (логин) администратора", "default"=>"root")
            , "superuser_mail" =>
                array("name"=>"Электронная почта администратора", "default"=>"root@example.com")
            , "superuser_password" =>
                array("name"=>"Пароль администратора (умолчание: root)", "default"=>"root", "type"=>"password")
            , "superuser_password2" =>
                array("name"=>"Повторите пароль", "default"=>"root", "type"=>"password")
            , "vk_id" =>
                array("name"=>"Идентификатор приложения ВКонтакте", "type"=>"string")
            , "vk_rights" =>
                array("name"=>"Список прав для ВК", "default"=>"notify,offline")
        );
    }
    /**
      * До начала установки проверять нечего
      * @return true в любом случае
      **/
    function initial_check()
    {
        return true;
    }
    /**
      * Будет вызвана для проверки после того, как
      * пользователь введет дополнительные параметры.
      * Проверяем, что пароли введены и совпадают, и что имя суперпользователя задано.
      * @param config массив параметров
      * @return true, если все в порядке (можно начинать установку)
      * или строку с описанием ошибки, если нельзя.
    **/
    function final_check($config)
    {
        if ($config["superuser_name"] == "") return "Please, fill in superuser name. ";
        if ($config["superuser_password"] == "") return "Please, fill in superuser password. ";
        if ($config["superuser_password"] != $config["superuser_password2"]) return "Passwords do not match.";
        return true;
    }
    /**
      * Эта функция должна полностью подчистить следы использования модуля.
      * @return true
      **/
    function uninstall()
    {
        // TODO: это баг -- удалять файл с кастомными настройками!
        @unlink("settings.php");
        return true;
    }
    /**
      * СамыйГлавныйМетод. Собственно, именно в нём
      * можно что-нибудь сделать с устанавливаемой системой.
      * В нашем случае пишем настройки в settings.php
      * @param config параметры, собранные при установке
      * @return true в случае успеха и строку с ошибкой в противном случае
      **/
    function install($config, &$logs)
    {
        global $engine_dir, $SETTINGS;
        require_once($SETTINGS["engine_dir"]."/sys/auth.php");
        $u = xcms_user();
        $u->set_superuser();
        $u->delete($config["superuser_name"]);
        $target = $u->create($config["superuser_name"], $config["superuser_mail"]);
        $target->passwd($config["superuser_password"]);
        $u->add_to_group($target->login(), "admin");
        $u->add_to_group($target->login(), "ank");
        $u->add_to_group($target->login(), "editor");
        $result = xcms_append("settings.php",
            "<?php\n".
            "\$auth_vk_id=\"${config['vk_id']}\";\n".
            "\$auth_vk_rights=\"${config['vk_rights']}\";\n".
            "?>");
        if (!$result)
            return "Cannot open settings.php for append. ";
        return true;
    }
    } // class AuthInstallHook

    /**
      * Объект необходимо инстанциировать в переменную с названием $hook
      **/
    $hook = new AuthInstallHook();
?>
