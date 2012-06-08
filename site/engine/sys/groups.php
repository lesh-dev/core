<?php
    function all_groups()
    {
        global $content_dir;
        $ans = array(
            "#all" => "Кто угодно"
            ,"#registered" => "Зарегистрированный"
            ,"#admin" => "Администратор"
            ,"#editor" => "Редактор"
            ,"#ank" => "Менеджер анкет"
        );
        $A = @getList("$content_dir/groups");
        if($A)
        {
            foreach($A as $k=>$v)
                $ans[$k] = $v;
        }
        return $ans;
    }
?>
