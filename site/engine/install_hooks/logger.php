<?php
    /**
      Это пример "инсталл-хука". Вы можете сделать 
      такой же, если Вы хотите контролировать 
      процедуру установки.
    **/
    class LoggerInstallHook
    {
        /** 
          Эта функция определяет название модуля 
          и не делает ничего больше **/
	function module_name()
	{
	    return "Logger Installer Hook";
	}
	/** 
	  Эта функция должна вернуть список переменных, 
	  необходимых модулю для функционирования
	**/
	function request_variables()
	{
	    //return array("another_var"=>array("name"=>"Samble Variable","type"=>"string","default"=>"def"));
	    return array();
	}
	/**
	  Эта функция будет вызвана для проверки, 
	  удовлетворяет ли система требованиям модуля. 
	  Должна вернуть true если да, или строку с 
	  описанием ошибки, если нет.
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
	    return true;
	}
    }
    
    /**
      Объект необходимо инстанциировать в переменную с названием $hook.
    **/
    $hook = new LoggerInstallHook();
?>