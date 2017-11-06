<?php

function xdesign_modern_sitelink($title, $link, $image_file_name)
{
    global $full_content_dir;
    global $pageid;

    $sitelink_page_prefix = "${full_content_dir}cms/pages/$pageid";
    $full_image_file_name = "${sitelink_page_prefix}/$image_file_name";
    $link_html = htmlspecialchars($link);
?>
    <a target="_blank" href="<?php echo $link_html; ?>">
        <div class="col-md-6">
            <div class="item-wrapper">
                <div class="row">
                    <div class="col-md-6 col-sm-6">
                        <img class="link_image" src="<?php echo $full_image_file_name; ?>" />
                    </div>
                    <div class="col-md-6 col-sm-6 about_person">
                        <h4><?php echo $title; ?></h4>
                    </div>
                </div>
            </div>
        </div>
    </a><?php
}

?>