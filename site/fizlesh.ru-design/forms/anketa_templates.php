<?php

/**
 * Anketa common footer
 */
function xcms_print_anketa_header() {
    global $engine_dir;
    global $engine_pub;
    global $xengine_dir;
    global $skin;
    ?>
    <script type="text/javascript" src="<?php echo $engine_pub; ?>/js/ank-validator.js"></script>
    <?php
    if ($skin == "modern")
        include(translate('<! css/design ank_modern.css !>'));
    if ($skin == "green")
        include(translate('<! css/design ank_green.css !>'));
    ?>
    <div class="ankLegend">
        <div><span class="ankAst Req">*</span> &#8211; обязательное поле</div>
        <div><span class="ankAst Gr">*</span> &#8211; должно быть заполнено хотя бы одно из полей</div>
        <div><span class="ankAst Rec">*</span> &#8211; рекомендуемое к заполнению поле</div>
    </div>
    <!-- <p>
        <b>Пожалуйста, указывайте <b>действующие</b> координаты для связи с&nbsp;Вами!</b>
        Если у&nbsp;Вас есть электронная почта, но Вы проверяете ящик <b>раз в&nbsp;полгода</b>,
        не&nbsp;указывайте его. Также, проверьте номера телефонов
        и&nbsp;e-mail перед отправкой анкеты.
    </p> -->
    <?php
}

function xcms_print_anketa_send_block() {?>
    <div class="ankRow">
            <?php xcmst_submit("submit_anketa", "Отправить"); ?>
        </div>
        <div class="ankMessageFrame" id="c-Message">
            <div class="ankError" id="t-Error">&nbsp;</div>
            <div class="ankWarning" id="t-Warning">&nbsp;</div>
        </div>
    <?php
}


/**
 * Anketa tail
 */
function xcms_print_anketa_footer() {?>
    <p>
        <b>P.S.</b> Мы не передаём полученную информацию третьим лицам,
        нам и без этого есть чем заняться.
    </p><?php
}

