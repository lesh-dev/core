<?php
	/** Simple logger:
	  * Logging now is as easy as killing bunnies with axes (c)
	  **/
    define('XLOG_DEBUG', 2);
    define('XLOG_INFO',  1);
    define('XLOG_ERROR', 0);
    function xcms_log_filename()
    {
	global $engine_dir;
	if(strlen($engine_dir) == 0) $ed = "engine";
	else $ed = $engine_dir;
	return "$ed/../engine.log";
    }
    function xcms_log($log_level, $message)
    {
    	global $engine_dir;
        $f = fopen(xcms_log_filename(), "a+");
        fwrite($f, "[".date('Y.m.d H:i:s')."]: $message\n");
        fclose($f);
    }

    function xcms_log_array($log_level, $name, $array)
    {
        global $engine_dir;
        $f = fopen(xcms_log_filename(), "a+");
        fwrite($f, "[".date('Y.m.d H:i:s')."]: ARRAY $name DUMP\n");
        foreach ($array as $key => $value)
            fwrite($f, "    '$key' => '$value'\n");
        fclose($f);
    }

?>