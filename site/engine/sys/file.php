<?php

/**
  * File operations library
  **/

function xcms_write($file_name, $contents)
{
    $f = @fopen($file_name, "wb");
    if (!$f)
        return false;
    $result = true;
    if (false === fwrite($f, $contents))
        $result = false;
    @fclose($f);
    return $result;
}

function xcms_append($file_name, $contents)
{
    $f = @fopen($file_name, "a+b");
    if (!$f)
        return false;
    $result = true;
    if (false === fwrite($f, $contents))
        $result = false;
    @fclose($f);
    return $result;
}

?>