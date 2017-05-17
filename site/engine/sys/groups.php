<?php
    function xcms_all_groups()
    {
        global $content_dir;
        $ans = array(
            "#all" => "Кто угодно",
            "#registered" => "Зарегистрированный",
            "#admin" => "Администратор",
            "#editor" => "Редактор",
            "#ank" => "Менеджер анкет",
            "#xsm-private" => "Менеджер конфиденциальных данных XSM",
        );
        $groups = xcms_get_list("$content_dir/groups");
        foreach ($groups as $key => $value)
            $ans[$key] = $value;
        return $ans;
    }
?>
