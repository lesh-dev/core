<?php
    $album_page_prefix = "${full_content_dir}cms/pages/$pageid";
    $cl = $_0;
    $name = $_1;
    $album_text = $_2;
    $album_img_name = "$album_page_prefix/$name.jpg";
    $album_arrow_name = "$album_page_prefix/arrow-$cl-small.png";
?><img
    class="album-<?php echo $cl; ?>"
    src="<?php echo $album_img_name; ?>"
    alt="<?php echo $name; ?>"
    title="<?php echo $name; ?>"
></img>
<p class="album-<?php echo $cl; ?>">
<img
    class="album-arrow-<?php echo $cl; ?>"
    src="<?php echo $album_arrow_name; ?>"
    alt="<?php echo $cl; ?> arrow"
></img>
<?php echo $album_text; ?></p>
<div style="clear: both;"></div>
