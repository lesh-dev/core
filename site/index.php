<?php
    if(file_exists("install.php"))
    {
        header("Location: install.php");
    }
    header("content-type: text/html; charset=utf-8");
    date_default_timezone_set('Europe/Moscow');
    include ("settings.php");
    include ("$engine_dir/.sys/settings.php");
    include ("$engine_dir/.sys/tag.php");
    include ("$engine_dir/.sys/ui.php");
    include ("$engine_dir/.sys/mailer.php");
    include ("$engine_dir/.sys/resample.php");
    /*if(@!$_GET["page"])
        $_GET["page"] = $SETTINGS["defaultpage"];
    if(!file_exists($_GET["page"].".xcms"))
    {
        $_GET["page"] = $SETTINGS["nopage"];
    }
    $tocompile = false;

    $f = fopen();*/


    function xcms_log($log_level, $message)
    {
        $f = fopen("engine.log", "a+");
        fwrite($f, "[".date('Y.m.d H:i:s')."]: $message.\n");
        fclose($f);
    }

    function setArgs($code,$outputStream)
    {
        global $SETTINGS;
        $argv = explode(" ",$code);
        fputs($outputStream, $SETTINGS["code_begin"]);
        foreach ($argv as $key=>$value)
        {
            fputs($outputStream,"\$code=\"$code\";");
            fputs($outputStream,"@\$argv[] = \"$value\";");
            if($key!=0)
            {
                //@$KEYLISTER[$value] = true;
                @fputs($outputStream,"@\$keys[\"$value\"] = true;");
                $a = explode("=", $value);
                @fputs($outputStream,"@\$param[\"{$a[0]}\"] = \"{$a[1]}\";");
                //@$PARAM[$key][$a[0]]=$a[1];
            }
        }
        fputs($outputStream, $SETTINGS["code_end"]);
    }

    function ParseString($s, $outputStream)
    {
        global $SETTINGS;
        $open = stristr($s,$SETTINGS["openbracket"]);
        if(!$open) {fputs($outputStream,$s); return;}
        $close = stristr($s,$SETTINGS["closebracket"]);
        $close = substr($close,strlen($SETTINGS["closebracket"]));
        $before = substr($s, 0, strlen($s) - strlen($open));

        fputs($outputStream,$before);


        $code = substr($open,strlen($SETTINGS["openbracket"])  );
        $code = substr($code,0,strlen($code)-strlen($close)-strlen($SETTINGS["closebracket"]));

        $code = trim($code);
        $argv = explode(" ",$code);

        $name = $argv[0];
        if(file_exists("{$SETTINGS["elementsdir"]}$name.php"))
        {
            include("{$SETTINGS["elementsdir"]}$name.php");
        }
        else
        {
            setArgs($code,$outputStream);
            if(file_exists("{$SETTINGS["elementsdir"]}$name.xcms"))
            {
                $newS = file_get_contents("{$SETTINGS["elementsdir"]}$name.xcms");
                foreach ($argv as $key=>$value)
                {
                    $newS = str_replace("%$key",$value,$newS);
                }
                $newS = str_replace("%*",$code,$newS);
                ParseString($newS,$outputStream);
            }
            elseif(file_exists("{$SETTINGS["elementsdir"]}$name.code"))
            {
                fputs($outputStream,file_get_contents("{$SETTINGS["elementsdir"]}$name.code"));
            }
            elseif(file_exists("{$SETTINGS["designdir"]}$name.template"))
            {
                fputs($outputStream,file_get_contents("{$SETTINGS["designdir"]}$name.template"));
            }
            else
            {
                xcms_log(0, "name is '$name', nopagecode: ".$SETTINGS["nopagecode"]);
                fputs($outputStream,file_get_contents("{$SETTINGS["elementsdir"]}{$SETTINGS["nopagecode"]}.code"));
            }
        }
        ParseString($close,$outputStream);
    }

    /*$f = fopen("outp.dat","w");
    ParseString ('BEFORE<!--! test !!-->AFTER',$f);
    fclose($f);
    echo file_get_contents("outp.dat");*/

    function compile($filename,$destination)
    {
        $toCompile = false;
        if(!file_exists($filename))
        {
            xcms_log(0, "Compiler fatal error: can't find source file '$filename'");
        }
        if(!file_exists($destination))$toCompile = true;
        else if(filemtime($filename)>filemtime($destination))
        {
            $toCompile = true;
        }
        if($toCompile)
        {
            xcms_log(1, "Compiling '$filename'");
            $f = fopen($destination, "w");
            if (!file_exists($filename)) {
                xcms_log(0, "Compile error: cannot find file '$filename'");
                return;
            }
            ParseString(file_get_contents($filename),$f);
            fclose($f);
        }
    }

    function translate($string)
    {
        global $SETTINGS;
        $fname = "{$SETTINGS["precdir"]}transl-".md5($string).".php";
        if(!file_exists($fname))
        {
            $f = fopen($fname,"w");
            $string = str_replace("<!","<#",$string);
            $string = str_replace("!>","#>",$string);
            ParseString($string,$f);
            fclose($f);
            $btname = $fname . ".backtrace";
            $f = fopen($btname, "w");
            fputs($f, $string);
            fclose($f);
        }
        return($fname);
    }

    // Choose filename
    $ref = @$_GET["ref"];
    if(!$ref) $ref = $SETTINGS["defaultpage"];
    if(file_exists("$design_dir/$ref.xcms"))
    {
        $rfile = "$design_dir/$ref.xcms";
    }
    elseif(file_exists("$engine_dir/global/$ref.xcms"))
    {
        $rfile = "$engine_dir/global/$ref.xcms";
    }
    else
    {
        $ref = "nopage.xcms";
        $rfile = "$design_dir/nopage.xcms";
    }

    // Find prec file
    compile($rfile, "{$SETTINGS["precdir"]}$ref.php");

    /*
    $toCompile = false;
    if(!file_exists("{$SETTINGS["precdir"]}$ref.php"))$toCompile = true;
    else if(filemtime("{$SETTINGS["documentsdir"]}$ref.xcms")>filemtime("{$SETTINGS["precdir"]}$ref.php"))
    {
        $toCompile = true;
    }
    //echo "*".filemtime("{$SETTINGS["documentsdir"]}$ref.xcms")."*<br>"."*".filemtime("{$SETTINGS["precdir"]}$ref.php")."*<br>";
    if($toCompile)
    {
        //echo  "Compile!";
        $f = fopen("{$SETTINGS["precdir"]}$ref.php","w");
        ParseString(file_get_contents("{$SETTINGS["documentsdir"]}$ref.xcms"),$f);
        fclose($f);
    }
    */

    include("{$SETTINGS["precdir"]}$ref.php");
?>

