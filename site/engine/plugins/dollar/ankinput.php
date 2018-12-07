<?php
// $_0 name
// $_1 type input|text
// $_2 title
// $_3 example
// $_4 req
// $_5 class

global $skin;

$ank_ele_name = $_0;
$ank_ele_type = $_1;
$ank_ele_title = $_2;
$ank_ele_example = $_3;
$ank_ele_req = $_4;
$ank_ele_class = $_5;
if ($ank_ele_req == "req") {
    $ank_ele_req = "<span class=\"ankAst Req\">*</span>";
} elseif ($ank_ele_req == "rec") {
    $ank_ele_req = "<span class=\"ankAst Rec\">*</span>";
} elseif ($ank_ele_req == "gr") {
    $ank_ele_req = "<span class=\"ankAst Gr\">*</span>";
} elseif ($ank_ele_req == "opt") {
    $ank_ele_req = "";
}

if ($ank_ele_type == "input") {?>
    <div class="ankRow">
        <span class="ankLabel"><?php echo $ank_ele_title; ?>:<?php echo $ank_ele_req; ?></span>
        <span class="ankValue">
            <input
                type="text"
                name="<?php echo $ank_ele_name; ?>"
                id="<?php echo $ank_ele_name; ?>-input"
                class="ank-input <?php echo $ank_ele_class; ?>"
            /><?php
            if (xu_not_empty($ank_ele_example)) {?>
                <div class="ankExample">Например: <?php echo $ank_ele_example; ?></div><?php
            }?>
        </span>
    </div>
<?php
} elseif ($ank_ele_type == "text") {
    if ($skin == "tidy") {?>
        <div class="ankRow">
            <span class="ankLabel"><?php echo $ank_ele_title; ?>:<?php echo $ank_ele_req; ?></span>
            <span class="ankValue">
            <textarea
                rows="3" cols="40"
                name="<?php echo $ank_ele_name; ?>" id="<?php echo $ank_ele_name; ?>-text"
                class="ank-text <?php echo $ank_ele_class; ?>"></textarea><?php
            if (xu_not_empty($ank_ele_example)) {?>
                <div class="ankExample">Например: <?php echo $ank_ele_example; ?></div><?php
            }?>
            </span>
        </div>
    <?php } else {?>
        <div class="ankRow">
            <span class="ankLabel">
                <?php echo $ank_ele_title; ?>:<?php echo $ank_ele_req; ?>
            </span>
        </div>
        <div class="ankRow"><textarea
            rows="3" cols="40"
            name="<?php echo $ank_ele_name; ?>" id="<?php echo $ank_ele_name; ?>-text"
            class="ank-text <?php echo $ank_ele_class; ?>"></textarea>
        </div><?php
        if (xu_not_empty($ank_ele_example)) {?>
            <div class="ankExample">Например: <?php echo $ank_ele_example; ?></div><?php
        }
    }
} else {
    echo "UNKNOWN ELEMENT TYPE '$ank_ele_name' detected when processing '$ank_ele_name'.<br/>\n";
}
?>