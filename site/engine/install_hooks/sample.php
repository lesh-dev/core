<?php
    /**
      * Это пример "инсталл-хука". Вы можете сделать
      * такой же, если Вы хотите контролировать
      * процедуру установки.
      **/
    class SampleInstallHook
    {
    /**
      * Определяет название модуля
      **/
    function module_name()
    {
        return "Just Sample";
    }
    /**
      * Список переменных, необходимых модулю для функционирования
      * @return key-value-массив переменных. Имя ключа -- название переменной,
      * значение -- массив с ключами name (название), type(тип переменной), default
      * значение по умолчанию. Например,
      * array(
      *     "param" => array(
      *         "name" => "Sample Variable One",
      *         "type" => "string",
      *         "default" => "def value",
      *     ),
      *     "another_var" => array(
      *         "name" => "Sample Variable Two",
      *         "type" => "string",
      *         "default" => "def",
      *     ),
      * );
      **/
    function request_variables()
    {
        return array();
    }
    /**
      * Проверяет, удовлетворяет ли система требованиям модуля.
      * @return true, если всё хорошо, и строку
      * с описанием ошибки, если нет. В данном примере никаких
      * проверок не делается, поэтому всегда отдаём true.
      **/
    function initial_check()
    {
        return true;
    }
    /**
      * Вызывается для проверки параметров, введённых пользователем.
      * @return true, если всё в порядке и можно начинать установку,
      * или строку с описанием ошибки, если всё плохо.
      **/
    function final_check($config)
    {
        return true;
    }
    /**
      * Подчищает следы использования модуля.
      * Например, если инсталлятор дописывает что-то в файл,
      * то этот метод должен файл удалить.
      **/
    function uninstall()
    {
        return true;
    }
    /**
      * СамыйГлавныйМетод. В нём следует выполнить действия по установке
      * модуля, используя параметры, полученные при настройке модуля
      * @param config параметры модуля
      * @return true, если установка удалась и строка с ошибкой
      * в противном случае
      **/
    function install($config, &$logs)
    {
        return true;
    }
    } // class SampleInstallHook

    /**
      * Объект необходимо инстанциировать в переменную с названием $hook.
      **/
    $hook = new SampleInstallHook();
?>