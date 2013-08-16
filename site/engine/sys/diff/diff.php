<?php
require_once("string.php");

function xsm_linear_diff($a, $b)
{
    $ai = 0;
    $bi = 0;
    $diff = "";
    $fuzz = 2;
    echo "<pre>".
        "<style>
            span.add { background-color: #ccffcc; }
            span.cut { text-decoration: line-through; background-color: #ffcccc; }
        </style>";
    while (true)
    {
        //echo "\n";
        $pat_a = xcms_substr($a, $ai, $fuzz);
        if (!xcms_len($pat_a))
            break;

        // seek for pat_a in b
        $pos_b = xcms_strpos($b, $pat_a, $bi);
        //echo "PAT_a=$pat_a, pos_b=$pos_b, rest=".xcms_substr($b, $bi, strlen($b))."\n";

        $pat_b = xcms_substr($b, $bi, $fuzz);
        if (!xcms_len($pat_b))
            break;

        // reversely, seek for pat_b in a
        $pos_a = xcms_strpos($a, $pat_b, $ai);
        //echo "PAT_b=$pat_b, pos_a=$pos_a, rest=".xcms_substr($a, $ai, strlen($a))."\n";
        if ($pos_a !== false && $pos_b !== false)
        {
            // both positions exist, choose minimal
            // deltas should be compared
            if ($pos_a - $ai < $pos_b - $bi)
            {
                // match in b is closer
                $diff .= '<span class="add">'.xcms_substr($a, $ai, $pos_a - $ai).'</span>'.$pat_b;
                $ai = $pos_a + $fuzz;
                $bi += $fuzz;
            }
            else
            {
                // match in a is closer
                $diff .= '<span class="add">'.xcms_substr($b, $bi, $pos_b - $bi).'</span>'.$pat_a;
                $bi = $pos_b + $fuzz;
                $ai += $fuzz;

            }
        }
        elseif ($pos_a !== false)
        {
            // match in b is closer
            $diff .= '<span class="add">'.xcms_substr($a, $ai, $pos_a - $ai).'</span>'.$pat_b;
            $ai = $pos_a + $fuzz;
            $bi += $fuzz;
        }
        elseif ($pos_b !== false)
        {
            // match in a is closer
            $diff .= '<span class="add">'.xcms_substr($b, $bi, $pos_b - $bi).'</span>'.$pat_a;
            $bi = $pos_b + $fuzz;
            $ai += $fuzz;
        }
        else
        {
            $diff .= '<span class="cut">'.xcms_substr($a, $ai, 1).'</span>';
            $ai++;
        }

    }
    // TODO: append tail
    echo $diff;
}

xsm_linear_diff("Хрен редьки не слаще!фффффф", "Хре_нy редьки  не слаще!aaфффффф");
xsm_linear_diff("проверка сбоем", "проверка боем");
xsm_linear_diff("проверка сбоем", "проверка Боем");
xsm_linear_diff("Иванов", "Сидоров");
xsm_linear_diff('$diff .= \'<span class=\"add\">\'.xcms_substr($a, $ai, $pos_a - $ai).\'</span>\'.$pat_b;',
    '$diff .= \'<span class=\'add\'>\'.xcms_substr($a, $ai, $pos_a - $ai).\"</span>\'.$pat_b;');

?>