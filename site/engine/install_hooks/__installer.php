<?php
    class InstallerInstallHook
    {
	function module_name()
	{
	    return "Основные настройки";
	}
	function request_variables()
	{
            global $SETTINGS;
            $design_list = glob("*design*", GLOB_ONLYDIR);
            if(count($design_list))
                $design = $design_list[0];
            else $design = "design";

            $content_list = glob("*content*", GLOB_ONLYDIR);
            if(count($content_list))
                $content = $content_list[0];
            else $content = "content";
            
            // set default values for *each* setting
            $SETTINGS["content_dir"] = "$content/";
            $SETTINGS["design_dir"]  = "$design/";
            $SETTINGS["engine_dir"]  = "engine/";
            $SETTINGS["engine_pub"]  = "engine_public/";
            //$SETTINGS["web_prefix"]  = ;
            $SETTINGS["mailer_enabled"] = true;
            
            return array(
              "content_dir" => array("name"=>"Содержимое сайта","default"=>"$content/")
              ,"design_dir" => array("name"=>"Дизайн","default"=>"$design/")
              ,"engine_dir" => array("name"=>"Движок","default"=>"engine/")
              ,"engine_pub" => array("name"=>"Публичное содержание движка","default"=>"engine_public/")
              ,"web_prefix" => array("name"=>"Префикс","default"=>substr(str_replace("install.php","",$_SERVER["REQUEST_URI"]),1))
              ,"mailer_enabled" => array("name"=>"Использовать ли оповещения по e-mail","default"=>"true", "type"=>"bool")
            );
            
	}
	function initial_check()
	{
            if (function_exists('apache_get_modules'))
            {
                $modules = apache_get_modules();
                $mod_rewrite = in_array('mod_rewrite', $modules);
            }
            else
                $mod_rewrite = getenv('HTTP_MOD_REWRITE')=='On' ? true : false;
            if(!$mod_rewrite)
	    {
		return "Apache mod_rewrite is not enabled. Please, configure Your apache server.";
	    }

            @mkdir(".prec", 0777);
            if($f = @fopen(".prec/.htaccess", "a"))
            {
                fputs($f,"deny from all");
                $PERM["prec"] = true;
                fclose($f);
            }
            else $PERM["prec"] = false;

            if($f = @fopen(".htaccess","a"))
            {
                $PERM["htaccess"] = true;
                fclose($f);
            }
            else $PERM["htaccess"] = false;

            if($f = @fopen("install.php","a"))
            {
                $PERM["install"] = true;
                fclose($f);
            }
            else $PERM["install"] = false;

            if($f = @fopen("settings.php","a"))
            {
                $PERM["settings"] = true;
                fclose($f);
            }
            else $PERM["settings"] = false;
	    
	    if(!$PERM["htaccess"])
	    {
              return "<p>Script can't write to root folder. You should do either</p>
            <ul>
                <li>Change rights to root folder to make it writeable</li>
                <li>create (writeable) folder .prec and empty writeable .htaccess file</li>
            </ul>";
	    }

            if(!$PERM["prec"])
              return "
                <p>Folder .prec/ is not writeable. Please fix this problem.</p>

                ";

            if(!$PERM["install"])
              return
              " <p>File ./install.php is not writeable. Please fix this problem.</p>
                ";

            if(!$PERM["settings"])
              return 
                " <p>File ./settings.php is not writeable. Please fix this problem.</p>
                ";
                
	    return true;
	}
	function final_check($config)
	{
            $dirs = array("content_dir","design_dir","engine_dir", "engine_pub");

            foreach ($dirs as $d)
                if(!is_dir(@$config[$d]))
                    return "$d variable is not a directory. ";
	    return true;
	}
	function uninstall()
	{
            @unlink("settings.php");
            return true;
        }
	function install($config)
	{
	    global $SETTINGS;
	    global $content_dir;
            $dirs = array("content_dir","design_dir","engine_dir", "engine_pub");

            $string_settings = array(
                'content_dir',
                'design_dir',
                'engine_dir',
                'engine_pub',
                'web_prefix'
            );
            $bool_settings = array(
                'mailer_enabled'
            );

            $f = fopen("settings.php", "a");
            fputs($f,"<?php\n");
            foreach($string_settings as $k)
            {
                // TODO: quotes escaping
                fputs($f, "\x20\x20\x20\x20\$$k = \"{$config["$k"]}\";\n");
            }
            foreach($bool_settings as $k)
            {
                $v = $config[$k]?"true":"false";
                fputs($f, "\x20\x20\x20\x20\$$k = $v;\n");
            }

            fputs($f,"\n?>");
	    fclose($f);
            include("settings.php");
            include("$engine_dir/sys/settings.php");
            include_once("$engine_dir/sys/tag.php");
            include_once("$engine_dir/cms/page_alias_func.php");
            include("$engine_dir/cms/rebuild_alias.xcms");
            include("$engine_dir/cms/build_rewrite.xcms");

            return true;
        }
    }
    $hook = new InstallerInstallHook();
?>