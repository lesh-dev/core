<?php
    /**
      * Logging now is as easy as killing bunnies with axes (c)
      **/
    define('XLOG_ERROR',    0);
    define('XLOG_WARNING',  1);
    define('XLOG_INFO',     2);
    define('XLOG_DEBUG',    3);

    // error codes for generic errors
    define('XE_WRONG_PASSWORD',       1000);
    define('XE_ACCESS_DENIED',        1001);

    // database errors
    define('XE_DB_OBJECT_NOT_FOUND',  2000);

    /**
      * Get a log file name
      * @return Log file name
      **/
    function xcms_log_filename()
    {
        global $meta_site_log_path;
        $log_path = $meta_site_log_path;
        if (!strlen($log_path))
        {
            global $engine_dir;
            $ed = strlen($engine_dir) ? $engine_dir : "engine";
            $log_path = "$ed/../engine.log";
        }
        return $log_path;
    }

    /**
      * Outputs message to log
      * @param log_level log level
      * @param message message to log (or anything convertable to string)
      **/
    function xcms_log($log_level, $message)
    {
        xcms_append(xcms_log_filename(), "[".xcms_datetime()."]: $message\n");
    }

    /**
      * Outputs an array to log
      * @param log_level log level
      * @param array name to put into log title
      * @param array array to log (or anything else that foreach construct works for)
      **/
    function xcms_log_array($log_level, $name, $array)
    {
        $output = "[".xcms_datetime()."]: ARRAY $name DUMP\n";
        foreach ($array as $key => $value)
            $output .= "    '$key' => '$value'\n";
        xcms_append(xcms_log_filename(), $output);
    }
?>