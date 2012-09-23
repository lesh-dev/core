<?php
    /**
      * @file logger.php
      * Simple logger:
      * Logging now is as easy as killing bunnies with axes (c)
      **/
    define('XLOG_DEBUG', 2);
    define('XLOG_INFO',  1);
    define('XLOG_ERROR', 0);

    /**
      * Get a log file name
      * @return Log file name
      **/
    function xcms_log_filename()
    {
        global $engine_dir;
        if (strlen($engine_dir) == 0) $ed = "engine";
        else $ed = $engine_dir;
        return "$ed/../engine.log";
    }

    /**
      * Outputs message to log
      * @param log_level log level
      * @param message message to log (or anything convertable to string)
      */
    function xcms_log($log_level, $message)
    {
        global $engine_dir;
        $f = fopen(xcms_log_filename(), "a+");
        fwrite($f, "[".date('Y.m.d H:i:s')."]: $message\n");
        fclose($f);
    }

    /**
      * Outputs an array to log
      * @param log_level log level
      * @param array name to put into log title
      * @param array array to log (or anything else that foreach construct works for)
      **/
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