<?
  header("Content-type: text/html; charset=UTF-8;");
?>
<h2>XCMS installer 2.0</h2>
<?
    function display_error($err)
    {
	echo "<font color=red>$err</font>";
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
    foreach($hooks as $hook)
    {
      foreach($hook->request_variables() as $k=>$v)
        $ALLVARS[$k] = $v;
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
        echo "<h3>Установка завершена!</h3>";
        echo "<a href=\"index.php\">Перейти к сайту</a>";
    }
    else
    {
      echo "<form method=\"post\"><h3>Шаг 1/2: выбор дополнительных параметров</h3>";
      echo "<table>";
      foreach($ALLVARS as $variable=>$v)
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
        echo "<tr><td>$name<td><input $typehack name=\"$variable\" value=\"$def\" />";
      }
      echo "</table>";
      echo "<input type=\"submit\" name=\"submit_variables\" value=\"Установить >>\">";
      echo "</form>";
    }
?>