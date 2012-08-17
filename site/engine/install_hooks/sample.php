<?
    // Every install hook is executed by installer and can make something nesessary for a module.
    // Install hook may:
    // a) Request variables to fill by user
    // b) Check something and if it is not correct -- fail.
    // c) Do something
    
    // Subclass and reimplement this object
    class SampleInstallHook
    {
	function module_name()
	{
	    return "Just Samble";
	}
	function request_variables()
	{
	    return array("another_var"=>array("name"=>"Samble Variable","type"=>"string","default"=>"def"));
	}
	function initial_check()
	{
	    return true;
	}
	function final_check($config)
	{
	    return true;
	}
	function uninstall()
	{
            return true;
	}
	function install($config)
	{
	    return true;
	}
    }
    $hook = new SampleInstallHook();
?>