<?php

function xcms_get_uploaded_file($file_id, $max_size = 15000000, $min_size = 128)
{
    $attachment = xcms_get_key_or($_FILES, $file_id, array());
    $file_name = xcms_get_key_or($attachment, "name");
    $tmp_name = xcms_get_key_or($attachment, "tmp_name");
    $size = xcms_get_key_or($attachment, "size");
    $error = xcms_get_key_or($attachment, "error");
    xcms_log(
        XLOG_INFO,
        "[ENGINE] Attachment data: ".
        "File name: '$file_name', ".
        "temp name: '$tmp_name', ".
        "size '$size' bytes, ".
        "error code: '$error'"
    );

    if ($size > $max_size ||
        $error == UPLOAD_ERR_INI_SIZE ||
        $error == UPLOAD_ERR_FORM_SIZE)
    {
        xcms_log(XLOG_ERROR, "[KERNEL] Uploaded file too large. Error: $error, size: $size");
        $attachment["exception_code"] = XE_FILE_TOO_LARGE;
        $attachment["max_size"] = $max_size;
    }
    elseif ($size < $min_size || xu_empty($file_name) || xu_empty($tmp_name))
    {
        xcms_log(XLOG_ERROR, "[KERNEL] File is empty or too small ($size while allowed $min_size)");
        $attachment["exception_code"] = XE_FILE_TOO_SMALL;
        $attachment["min_size"] = $min_size;
    }
    elseif ($error !== 0)
    {
        xcms_log(XLOG_ERROR, "[KERNEL] Unknown file upload error: $error");
        $attachment["exception_code"] = XE_FILE_UPLOAD_ERROR;
    }
    else
    {
        $attachment["exception_code"] = 0;
    }
    return $attachment;
}