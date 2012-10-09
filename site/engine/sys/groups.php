<?php
    function xcms_all_groups()
    {
        global $content_dir;
        $ans = array(
            "#all" => "Кто угодно"
            ,"#registered" => "Зарегистрированный"
            ,"#admin" => "Администратор"
            ,"#editor" => "Редактор"
            ,"#ank" => "Менеджер анкет"
        );
        $groups = xcms_get_list("$content_dir/groups");
        foreach($groups as $k=>$v)
            $ans[$k] = $v;
        return $ans;
    }
    /// Deprecated! Use xcms_all_groups instead!
    function all_groups()
    {
        return xcms_all_groups();
    }
?>
