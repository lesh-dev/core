<?php

function xdesign_modern_contact(
    $contact_id,  // something unique, e.g. XCMS login, etc)
    $last_name = "",
    $first_name = "",
    $job = "",
    $phone = "",
    $email = "",
    $social_profile = "",
    $xsm_id = false,
    $image_name = "",
    $description = ""
) {
    global $full_content_dir;
    global $pageid;

    $contact_page_prefix = "${full_content_dir}cms/pages/$pageid";
    $full_image_file_name = "${contact_page_prefix}/$image_name";
    $link_html = htmlspecialchars($link);
    $fio = "$first_name $last_name";
?>
    <div class="col-md-12">
        <div class="item-wrapper">
            <div class="row">
                <div class="col-md-4 col-sm-6">
                    <img class="ava_image" src="<?php echo $full_image_file_name; ?>" alt="<?php echo $fio; ?>" />
                </div>
                <div class="col-md-6 col-sm-6 about_person">
                <h4><?php echo $fio; ?></h4>
                <p><?php echo $job; ?></p>
                <?php
                if (xu_not_empty($phone)) {?>
                    <p><a href="tel:<?php echo $phone; ?>"><?php echo $phone; ?></a></p><?php
                }
                if (xu_not_empty($social_profile))
                {
                    $social_profile_link = $social_profile;
                    // TODO(mvel): wrap social profile handling
                    if (xu_substr($social_profile, 0, 4) != "http")
                    {
                        if (xu_substr($social_profile, 0, 5) == "vk.com")
                        {
                            $social_profile_link = "https://$social_profile";
                        }
                    }
                    $social_profile = str_replace("http://", "", $social_profile);
                    $social_profile = str_replace("https://", "", $social_profile);
                    ?>
                    <p><a href="<?php echo $social_profile_link; ?>"><?php echo $social_profile; ?></a></p><?php
                }
                ?>
                <p><a href="mailto:<?php echo $email; ?>"><?php echo $email; ?></a></p>
          </div>
        </div>
      </div>
    </div>
<?php
}

?>