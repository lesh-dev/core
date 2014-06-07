<?php
    function xcms_set_args($code, $output_stream)
    {
        global $SETTINGS;
        $argv = explode(EXP_SP, $code);
        fputs($output_stream, $SETTINGS["code_begin"]);
        foreach ($argv as $key=>$value)
        {
            fputs($output_stream, "\$code=\"$code\";");
            fputs($output_stream, "@\$argv[] = \"$value\";");
            if($key!=0)
            {
                // singular value is a boolean switch
                $a = explode(EXP_EQ, $value);
                if (count($a) >= 2)
                    @fputs($output_stream, "@\$param[\"{$a[0]}\"] = \"{$a[1]}\";");
                else
                    @fputs($output_stream, "@\$param[\"{$a[0]}\"] = true;");
            }
        }
        fputs($output_stream, $SETTINGS["code_end"]);
    }

    function xcms_parse_string($s, $output_stream)
    {
        global $SETTINGS;
        $open = stristr($s, $SETTINGS["openbracket"]);
        if (!$open)
        {
            fputs($output_stream, $s);
            return;
        }
        $close = stristr($s, $SETTINGS["closebracket"]);
        $close = substr($close, strlen($SETTINGS["closebracket"]));
        $before = substr($s, 0, strlen($s) - strlen($open));

        fputs($output_stream, $before);

        $code = substr($open, strlen($SETTINGS["openbracket"])  );
        $code = substr($code, 0, strlen($code)-strlen($close)-strlen($SETTINGS["closebracket"]));

        $code = trim($code);
        $argv = explode(EXP_SP, $code);

        $name = $argv[0];
        $elem_full_name = $SETTINGS["engine_dir"].$name;
        $template_full_name = $SETTINGS["design_dir"]."$name.template";

        if(file_exists("$elem_full_name.php"))
        {
            include("$elem_full_name.php");
        }
        else
        {
            xcms_set_args($code, $output_stream);
            $full_name = "$elem_full_name.xcms";
            if (!file_exists($full_name))
                $full_name = "${elem_full_name}default.xcms";
            if (file_exists($full_name))
            {
                $new_contents = file_get_contents($full_name);
                foreach ($argv as $key=>$value)
                    $new_contents = str_replace("%$key", $value, $new_contents);
                // replace all unused parameters with empty strings
                $new_contents = preg_replace('/%[0-9]/', '', $new_contents);
                // replace wildcarded arguments
                $new_contents = str_replace("%*", $code, $new_contents);
                xcms_parse_string($new_contents, $output_stream);
            }
            elseif(file_exists("$elem_full_name.code"))
            {
                fputs($output_stream, file_get_contents("$elem_full_name.code"));
            }
            elseif(file_exists($template_full_name))
            {
                fputs($output_stream, file_get_contents($template_full_name));
            }
            else
            {
                xcms_log(XLOG_ERROR, "[COMPILER] name is '$name', nopagecode: ".$SETTINGS["nopagecode"]);
                fputs($output_stream, file_get_contents("{$SETTINGS["engine_dir"]}{$SETTINGS["nopagecode"]}.code"));
            }
        }
        xcms_parse_string($close, $output_stream);
    }

    function xcms_compile($filename, $destination)
    {
        $to_compile = false;
        if (!file_exists($filename))
        {
            xcms_log(XLOG_ERROR, "[COMPILER] Fatal error: can't find source file '$filename'");
        }
        if (!file_exists($destination))
            $to_compile = true;
        elseif (@filemtime($filename) > @filemtime($destination))
        {
            $to_compile = true;
        }

        if ($to_compile)
        {
            xcms_log(XLOG_INFO, "[COMPILER] Compiling '$filename'");
            $f = fopen($destination, "w");
            if (!file_exists($filename)) {
                xcms_log(XLOG_ERROR, "[COMPILER] Compile error: cannot find file '$filename'");
                return;
            }
            xcms_parse_string(file_get_contents($filename), $f);
            fclose($f);
        }
    }

    function translate($string)
    {
        global $SETTINGS;
        $fname = "{$SETTINGS["precdir"]}transl-".md5($string).".php";
        if(!file_exists($fname))
        {
            $f = fopen($fname, "w");
            $string = str_replace("<!", "<#", $string);
            $string = str_replace("!>", "#>", $string);
            xcms_parse_string($string, $f);
            fclose($f);
            xcms_write("$fname.backtrace", $string);
        }
        return($fname);
    }

    function xcms_main($refname = "")
    {
        global $SETTINGS, $engine_dir, $design_dir;
        global $main_ref_file;
        global $main_ref_name;
        global $ref;

        // Choose filename
        if(strlen($refname) != 0 )
        {
            $ref = $refname;
        }
        else
        {
            $ref = @$_GET["ref"];
        }

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
        $main_ref_name = "{$SETTINGS["precdir"]}f$refname-$ref.php";
    }
?>