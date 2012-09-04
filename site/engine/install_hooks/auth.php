<?php
    /**
      Это пример "инсталл-хука". Вы можете сделать 
      такой же, если Вы хотите контролировать 
      процедуру установки.
    **/
    class AuthInstallHook
    {
        /** 
          Эта функция определяет название модуля 
          и не делает ничего больше **/
	function module_name()
	{
	    return "Пользователи, права и доступ";
	}
	/** 
	  Эта функция должна вернуть список переменных, 
	  необходимых модулю для функционирования
	**/
	function request_variables()
	{
	    return array(
                "superuser_name" => array("name"=>"Имя (логин) администратора","default"=>"root")
                ,"superuser_mail" => array("name"=>"Электронная почта администратора","default"=>"root@example.com")
	        ,"superuser_password" => array("name"=>"Пароль администратора (умолчание: root)","default"=>"root","type"=>"password")
	        ,"superuser_password2" => array("name"=>"Повторите пароль","default"=>"root","type"=>"password")
		,"vk_id"=>array("name"=>"Идентификатор приложения ВКонтакте","type"=>"string")
		,"vk_rights"=>array("name"=>"Список прав для ВК","default"=>"notify,offline")
	    );
	}
	/**
	  Эта функция будет вызвана для проверки, 
	  удовлетворяет ли система требованиям модуля. 
	  Должна вернуть true если да, или строку с 
	  описанием ошибки, если нет.
	**/
	function initial_check()
	{
	    return true;
	}
	/**
          Эта функция будет вызвана для проверки после 
          того, как пользователь введет дополнительные 
          параметры. Должна вернуть true если все в порядке 
          и можно начинать установку, или строку с описанием 
          ошибки, если нет.
	**/
	function final_check($config)
	{
            if($config["superuser_name"] == "") return "Please, fill in superuser name";
            if($config["superuser_password"] == "") return "Please, fill in superuser password";
            if($config["superuser_password"] != $config["superuser_password2"])return "Passwords does not match.";
	    return true;
	}
	/** 
          Эта функция должна полностью подчистить следы использования модуля.
          Например, если инсталлятор дописывает что-то в файл, то этот метод должен файл удалить.
	**/
	function uninstall()
	{
	    @unlink("settings.php");
            return true;
	}
	/**
	  Самый Главный Метод. Собственно, именно в нем можно что-нибудь сделать с устанавливаемой системой.
	**/
	function install($config)
	{
            global $engine_dir, $SETTINGS;
            require_once($SETTINGS["engine_dir"]."/sys/auth.php");
            $u = xcms_user();
            $u->setSuperuser();
            $u->delete($config["superuser_name"]);
            $target = $u->create($config["superuser_name"],$config["superuser_mail"]);
            $target->passwd($config["superuser_password"]);
            $u->groupadd($target->login(), "admin");
            $f = fopen("settings.php","a");
	    fputs($f,"<?php \$auth_vk_id=\"${config['vk_id']}\"; ?>\n");
	    fputs($f,"<?php \$auth_vk_rights=\"${config['vk_rights']}\"; ?>\n");
	    return true;
	}
    }
    
    /**
      Объект необходимо инстанциировать в переменную с названием $hook.
    **/
    $hook = new AuthInstallHook();
?>
