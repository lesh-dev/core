<?php
    header("Content-type: text/html; charset=UTF-8;");
?>
<html>
    <head>
        <title>XCMS Installer 2.0</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    </head>
    <body>
        <style><?php echo "\n".@file_get_contents('install.css')."\n"; ?></style>
        <h1>Установка XCMS 2.0</h1>
<?php
    require_once("engine/sys/tag.php");
    require_once("engine/sys/logger.php");

    function display_error($err)
    {
        echo "<span style=\"color: red\">$err</span>\n";
    }

    $hookls = glob("engine/install_hooks/*.php");
    $hooks = array();
    foreach($hookls as $hookfile)
    {
        unset($hook);
        require $hookfile;
        if (isset($hook))
        {
            $hooks[] = $hook;
        }
    }
    $ok = true;
    // check if it's all OK
    foreach($hooks as $hook)
    {
        $ans = $hook->initial_check();
        if($ans === TRUE)
        {
            //echo "<li>Test passed..";
        }
        else
        {
            display_error($ans);
            $ok = false;
        }
    }
    $ALLVARS = array();
    $ALLSECVARS = array();
    foreach($hooks as $hook)
    {
        if (!isset($ALLSECVARS[$hook->module_name()]))
            $ALLSECVARS[$hook->module_name()] = array();
        foreach($hook->request_variables() as $k=>$v)
        {
            $ALLVARS[$k] = $v;
            $ALLSECVARS[$hook->module_name()][$k] = $v;
        }
    }
    if(!$ok)
    {
        die("<br/>Installation will not be continued until You will not take action.");
    }
    if (@$_POST["submit_variables"])
    {
        // Handle them
        foreach($hooks as $hook)
        {
            $ans = $hook->final_check(@$_POST);
            if($ans === TRUE) continue;
            display_error($ans);
            die();
        }
        foreach($hooks as $hook)
        {
            $ans = $hook->uninstall();
            if($ans === TRUE) continue;
            display_error($ans);
            die();
        }
        foreach($hooks as $hook)
        {
            $ans = $hook->install(@$_POST);
            if($ans === TRUE) continue;
            display_error($ans);
            die();
        }
        unlink("install.php");
        ?>
        <h3>Установка завершена!</h3>
        <a href="index.php">Перейти к сайту</a>
        <?php
    }
    else
    {
        ?>
        <form method="post">
            <h3>Шаг 1/2: выбор дополнительных параметров</h3>
            <table>
        <?php
        foreach($ALLSECVARS as $hook_name=>$hook_variables)
        {
            if(count($hook_variables))
                echo "<tr><td colspan=\"2\" class=\"hook-name\">$hook_name</td></tr>\n";
            foreach($hook_variables as $variable=>$v)
            {
                $name = @$v["name"];
                if($name === FALSE)
                    $name = $variable;
                $type = @$v["type"];
                if($type === FALSE)
                    $type = "string";
                $def = @$v["default"];
                $typehack = "";
                if($type == "bool" || $type == "boolean")
                {
                    $typehack = "type=\"checkbox\"";
                    if($def == "true") $typehack .= " checked";
                }
                if($type == "password") $typehack = "type=\"password\"";
                echo "<tr><td class=\"key\">$name</td>".
                    "<td><input $typehack name=\"$variable\" id=\"$variable\" value=\"$def\" /></td></tr>\n";
            }
        }
        ?>
            </table>
            <input type="submit" name="submit_variables" value="Установить &gt;&gt;" />
        </form>
        <?php
    }
?>
</body>
</html>