<?php
include("$engine_dir/contest/scheme.php");
include("$engine_dir/contest/action.php");

// redefine it
$CONTEST_CURRENT_YEAR = $_0;
$FILTER = "( contest_year = \"$CONTEST_CURRENT_YEAR\" )";

$probs = xdb_get_table("problems", $FILTER);
$works = ctx_get_works();

$results = ctx_calculate_results($works, $probs);

$done = $results['done'];
$done_sum = $results['done_sum'];

?>
<table class="contest-results">
<thead><tr><th>#</th><th>Имя</th><th>Результат</th></tr></thead>
<?php
$i = 1;
foreach ($done_sum as $sum)
    foreach ($done[$sum] as $work)
    {
        echo "<tr><td>$i</td>".ctx_print_result_row($work, $probs, true)."</tr>\n";
        $i++;
    }
?></table><?php
?>