<?php
    header("Content-type: text/html; charset=UTF-8;");
    $target_version = @file_get_contents("VERSION");

    function xsm_insert_style($css) {
        echo "<style>\n$css\n</style>";
    }

?><!DOCTYPE html>
<html>
    <head>
        <title>XCMS Installer <?php echo $target_version; ?></title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    </head>
    <body>
        <?php
            xsm_insert_style(@file_get_contents("install.css"));
        ?>
        <h1>Установка XCMS <?php echo $target_version; ?></h1>
<?php
    $engine_dir = "engine/";  // some initial hardcode. TODO: make autodetection
    require_once("${engine_dir}sys/string.php");
    require_once("${engine_dir}sys/tag.php");
    require_once("${engine_dir}sys/controls.php");
    require_once("${engine_dir}sys/logger.php");
    require_once("${engine_dir}sys/file.php");
    require_once("${engine_dir}sys/util.php");

    function display_error($err)
    {
        echo "<span style=\"color: red\">$err</span>\n";
    }

    $hookls = glob("${engine_dir}install_hooks/*.php");
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
        if ($ans === true)
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
    if (!$ok)
    {
        die("<p>Installation will not be continued until you will not take action.</p>");
    }
    if (@$_POST["submit_variables"])
    {
        // Handle them
        foreach ($hooks as $hook)
        {
            $ans = $hook->final_check(@$_POST);
            if ($ans === true) continue;
            display_error($ans);
            die();
        }
        foreach($hooks as $hook)
        {
            $ans = $hook->uninstall();
            if ($ans === true) continue;
            display_error($ans);
            die();
        }
        foreach($hooks as $hook)
        {
            $logs = "";
            $ans = $hook->install(@$_POST, $logs);
            if ($ans === true) continue;
            display_error($ans);
            die();
        }
        $fi = @fopen("install.php", "w");
        fclose($fi);
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
            if (count($hook_variables))
                echo "<tr><td colspan=\"2\" class=\"hook-name\">$hook_name</td></tr>\n";
            foreach($hook_variables as $variable=>$v)
            {
                $name = @$v["name"];
                if ($name === false)
                    $name = $variable;
                $type = @$v["type"];
                if ($type === false)
                    $type = "string";
                $def = @$v["default"];
                $typehack = "";
                if ($type == "bool" || $type == "boolean")
                {
                    $typehack = "type=\"checkbox\"";
                    if ($def == "true")
                        $typehack .= ' checked="checked"';
                }
                if ($type == "password")
                    $typehack = "type=\"password\"";
                echo "<tr><td class=\"key\">$name</td><td>";
                // checkbox hack
                if ($type == "bool" || $type == "boolean")
                    echo "<input type=\"hidden\" name=\"$variable\" value=\"\" />";
                if (xu_empty($typehack))
                    $typehack = "type=\"text\"";
                echo "<input $typehack name=\"$variable\" id=\"$variable\" value=\"$def\" /></td></tr>\n";
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