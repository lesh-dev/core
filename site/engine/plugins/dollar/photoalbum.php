<?php
    $album_page_prefix = "${full_content_dir}cms/pages/$pageid";
    $cl = $_0;
    $name = $_1;
    $album_text = $_2;
    $album_img_name = "$album_page_prefix/$name.jpg";
?>
<div class="photoalbum-block">
    <img
        class="photoalbum-<?php echo $cl; ?>"
        src="<?php echo $album_img_name; ?>"
        alt="<?php echo $name; ?>"
        title="<?php echo $name; ?>"
    ></img>
    <p class="photoalbum-<?php echo $cl; ?>">
    <?php echo $album_text; ?></p>
</div>
<div class="photoalbum-div" style="clear: both;"></div>
