<?php
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
        if(!$open)
        {
            fputs($outputStream,$s);
            return;
        }
        $close = stristr($s,$SETTINGS["closebracket"]);
        $close = substr($close,strlen($SETTINGS["closebracket"]));
        $before = substr($s, 0, strlen($s) - strlen($open));

        fputs($outputStream,$before);


        $code = substr($open,strlen($SETTINGS["openbracket"])  );
        $code = substr($code,0,strlen($code)-strlen($close)-strlen($SETTINGS["closebracket"]));

        $code = trim($code);
        $argv = explode(' ', $code);

        $name = $argv[0];
        $elem_full_name = $SETTINGS["elementsdir"].$name;
        $template_full_name = $SETTINGS["designdir"]."$name.template";

        if(file_exists("$elem_full_name.php"))
        {
            include("$elem_full_name.php");
        }
        else
        {
            setArgs($code, $outputStream);
            $full_name = "$elem_full_name.xcms";
            if (!file_exists($full_name))
                $full_name = "${elem_full_name}default.xcms";
            if (file_exists($full_name))
            {
                $newS = file_get_contents($full_name);
                foreach ($argv as $key=>$value)
                {
                    $newS = str_replace("%$key",$value,$newS);
                }
                $newS = str_replace("%*",$code,$newS);
                ParseString($newS,$outputStream);
            }
            elseif(file_exists("$elem_full_name.code"))
            {
                fputs($outputStream, file_get_contents("$elem_full_name.code"));
            }
            elseif(file_exists($template_full_name))
            {
                fputs($outputStream,file_get_contents($template_full_name));
            }
            else
            {
                xcms_log(0, "name is '$name', nopagecode: ".$SETTINGS["nopagecode"]);
                fputs($outputStream,file_get_contents("{$SETTINGS["elementsdir"]}{$SETTINGS["nopagecode"]}.code"));
            }
        }
        ParseString($close,$outputStream);
    }

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

    function xcms_main()
    {
        global $SETTINGS, $engine_dir, $design_dir;
        global $main_ref_file;
        global $main_ref_name;
        global $ref;

        // Choose filename
        $ref = @$_GET["ref"];
        if (!$ref) $ref = $SETTINGS["defaultpage"];
        if (file_exists("$design_dir/$ref.xcms"))
        {
            $main_ref_file = "$design_dir/$ref.xcms";
        }
        elseif(file_exists("$engine_dir/global/$ref.xcms"))
        {
            $main_ref_file = "$engine_dir/global/$ref.xcms";
        }
        else
        {
            $ref = "nopage.xcms";
            $main_ref_file = "$design_dir/nopage.xcms";
        }

        // Find prec file
        $main_ref_name = "{$SETTINGS["precdir"]}$ref.php";
    }
?>