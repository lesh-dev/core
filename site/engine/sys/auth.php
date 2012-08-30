<?php
    require_once("$engine_dir/sys/tag.php");
    /**
	This one returns file name by user's name
    **/
    function auth_filename($user)
    {
	global $content_dir;
	return "$content_dir/auth/usr/$user.usr";
    }
    /**
	Counts saulted hash.
    **/
    function auth_hash($string)
    {
	return md5($string."Thisisasault!");
    }
    /** 
	This one returns user by it's username. If username is not specified, current user is determined and returned.
    **/
    function auth_user()
    {
	return FALSE;
    }
    /**
	This one returns true if user created succesfully or String with error
    **/
    function auth_create_user($login, $primary_group=NULL)
    {
	if(strlen($login) == 0) return "Empty login!";
	$fn = auth_filename($login);
	if(file_exists($fn)) return "This user is already presented!";
	$USER = array("name"=>$login);
	if($primary_group !== NULL)
	    $USER["group"] = $primary_groups;
	if(!xcms_save_list($fn, $USER)) return "Unknown error; Maybe -- chmod problem.";
	return TRUE;
    }
    /**
	Changes password of user.
    **/
    function auth_passwd()
    {
	if(strlen($login) == 0) return "Empty login!";
    }
    function get_groups()
    {
    }
?>
<h3>Compiled</h3>
<?php
    echo auth_create_user("test");
?>