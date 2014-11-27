<?php
    $album_page_prefix = "${full_content_dir}cms/pages/$pageid";
    $album_img_name = "${album_page_prefix}/${_0}.jpg";
    $album_arrow_name = "${album_page_prefix}/arrow-left-small.png";
?><img
    class="album-left"
    src="<?php echo $album_img_name; ?>"
    alt="<?php echo $_0; ?>"
    title="<?php echo $_0; ?>"
></img>
<p class="album-left">
<img
    class="album-arrow-left"
    src="<?php echo $album_arrow_name; ?>"
    alt="left arrow"
></img>
<?php echo $_1; ?></p>
<div style="clear: both;"></div>
