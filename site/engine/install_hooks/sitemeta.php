<?php
    /**
      Это пример "инсталл-хука". Вы можете сделать 
      такой же, если Вы хотите контролировать 
      процедуру установки.
    **/
    class MetaInfoHook
    {
        /** 
          Эта функция определяет название модуля 
          и не делает ничего больше **/
	function module_name()
	{
	    return "Общая информация о веб-сайте";
	}
	/** 
	  Эта функция должна вернуть список переменных, 
	  необходимых модулю для функционирования
	**/
	function request_variables()
	{
	    return array(
	      "site_name"=>array("name"=>"Название веб-сайта","type"=>"string","default"=>$_SERVER["HTTP_HOST"])
	      ,"site_url"=>array("name"=>"Адрес веб-сайта","type"=>"string","default"=>"http://{$_SERVER['HTTP_HOST']}".str_replace("install.php","",$_SERVER["REQUEST_URI"]))
	      ,"webmaster_mail"=>array("name"=>"Адрес службы техподдержки","type"=>"string","default"=>"support@".$_SERVER["HTTP_HOST"])
	    );
	    //return array();
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
	    return true;
	}
	/** 
          Эта функция должна полностью подчистить следы использования модуля.
          Например, если инсталлятор дописывает что-то в файл, то этот метод должен файл удалить.
	**/
	function uninstall()
	{
            return true;
	}
	/**
	  Самый Главный Метод. Собственно, именно в нем можно что-нибудь сделать с устанавливаемой системой.
	**/
	function install($config)
	{
	    $f = fopen("settings.php","a");
	    fputs($f,"\n<?php /** This block was inserted by installer -- sitemeta.php. Edit it, but it can be regenerated. **/");
	    fputs($f,"\n   \$meta_site_name = '".$config["site_name"]."';");
	    fputs($f,"\n   \$meta_site_url = '".$config["site_url"]."';");
	    fputs($f,"\n   \$meta_site_mail = '".$config["webmaster_mail"]."';");
	    fputs($f,"\n/** sitemeta.php hook : end **/ ?>\n");
	    return true;
	}
    }
    
    /**
      Объект необходимо инстанциировать в переменную с названием $hook.
    **/
    $hook = new MetaInfoHook();
?>