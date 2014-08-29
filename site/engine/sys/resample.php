<?php
    $rezX = 0;
    $rezY = 0;

    /**
      * @param sizeType is 'X' (to make resize based on X dimension
      * with preserving aspect ratio) or any other value
      **/
    function resizeJPEG($fileFrom, $fileTo, $newSize, $sizeType, $JPEGQuality = 100)
    {
        global $rezX;
        global $rezY;

        $source = imagecreatefromjpeg($fileFrom);
        if (xu_empty($source))
        {
            echo "<b>Can't open image '$fileFrom'</b>";
            return;
        }
        $srcX = imagesx($source);
        $srcY = imagesy($source);
        if ($sizeType == 'X')
            $ratio = $newSize / $srcX;
        else  $ratio = $newSize / $srcY;
        $destX = $srcX * $ratio;
        $destY = $srcY * $ratio;
        $destImage = imagecreateTrueColor($destX, $destY);

        imagecopyresampled($destImage, $source, 0, 0, 0, 0, $destX, $destY, $srcX, $srcY);
        imagejpeg($destImage, $fileTo, $JPEGQuality);
        imagedestroy($source);
        imagedestroy($destImage);
        $rezX = (int)$destX;
        $rezY = (int)$destY;
        if (file_exists($fileTo))
            return true;
        return false;
    }

    function make640($fileFrom, $fileTo, $JPEGQuality = 75)
    {
        $source = imagecreatefromjpeg($fileFrom);
        $srcX = imagesx($source);
        $srcY = imagesy($source);
        imagedestroy($source);
        if ($srcX > $srcY)
        {
            $type = 'Y';
            $dest = 480;
        }
        else
        {
            $type = 'X';
            $dest = 480;
        }
        return resizeJPEG($fileFrom, $fileTo, $dest, $type, $JPEGQuality);
    }

    function preview($fileFrom, $fileTo, $size = 100, $JPEGQuality = 75)
    {
        return resizeJPEG($fileFrom, $fileTo, $size, 'Y', $JPEGQuality);
    }
?>