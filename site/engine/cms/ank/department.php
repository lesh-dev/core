<?php

function xsm_draw_department_selector($value, $name = 'department_id')
{
    echo xsm_make_selector(
        'department',
        $name,
        $value,
        array('department_title'),
        "(1 = 1) ORDER BY (department_id = 2), department_title"
    );
}

?>