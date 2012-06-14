<?php
	/** Simple logger:
	  * Logging now is as easy as killing bunnies with axes (c)
	  **/
    function xcms_log($log_level, $message)
    {
    	global $engine_dir;
        $f = fopen("$engine_dir/../engine.log", "a+");
        fwrite($f, "[".date('Y.m.d H:i:s')."]: $message\n");
        fclose($f);
    }
?>