<?php

function xcms_print_anketa_header() {
    global $engine_dir;
    global $xengine_dir;
    global $skin;
    ?>
    <script type="text/javascript" src="${engine_pub}/js/ank-validator.js"></script>
    <?php
    if ($skin == "modern")
        include(translate('<! css/design ank_modern.css !>'));
    else
        include(translate('<! css/design ank_green.css !>'));
    ?>
    <div class="ankLegend">
        <div><span class="ankAst Req">*</span> &#8211; обязательное поле</div>
        <div><span class="ankAst Gr">*</span> &#8211; должно быть заполнено хотя бы одно из полей</div>
        <div><span class="ankAst Rec">*</span> &#8211; рекомендуемое к заполнению поле</div>
    </div>
    <p>
        <b>Пожалуйста, указывайте <b>действующие</b> координаты для связи с&nbsp;Вами!</b>
        Если у&nbsp;Вас есть электронная почта, но Вы проверяете ящик <b>раз в&nbsp;полгода</b>,
        не&nbsp;указывайте его. Также, проверьте номера телефонов
        и&nbsp;e-mail перед отправкой анкеты.
    </p><?php
}

function xcms_print_anketa_footer() {?>
    <p>
        <b>P.S.</b> Мы не передаём полученную информацию третьим лицам,
        нам и без этого есть чем заняться.
    </p><?php
}

