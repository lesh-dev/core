<?php
 $mailmsg = "===================================\n";
 $rssfeed = "&lt;table&gt;";
 $filename = "".date("Y-m-d",mktime())."-".mktime()."".".html";
 $f = fopen("ank/$filename","w");
 fputs($f,"Date: ".date("r")."\n");
 fputs($f,"<table>");
 $name = "Школьнег";
 foreach (@$_POST as $key=>$value) 
 {
	if ($key == "Familiya")
		$name = $value;
 	fputs($f,"<tr><td>$key</td><td>\t$value</td></tr><br>\n");
	$mailmsg .= "\n$key\t$value";
	$rssfeed .= "&lt;tr&gt;&lt;td&gt;$key&lt;/td&gt;&lt;td&gt;$value&lt;/td&gt;&lt;/tr&gt;";
 }
 $rssfeed .= "&lt;/table&gt;";
 fputs($f,"</table>");
 fclose($f);
 //$f = fopen("ank/lastdate");
 //fputs($f,date("r"));
 //fclose(f);
 include_once("elem/cms/addrssfeed.php");
 addrssfeed("Пришла новая анкета", $rssfeed, "http://fizlesh.ru/ank/$filename", $name);

 mail("serge19746@yandex.ru","anketko",$mailmsg);
 mail("demarin@mail.ru","anketko",$mailmsg);
?>
<h1>Спасибо! Ваша анкета принята!</h1>
Подождите...
<meta http-equiv="refresh" content="2;URL=index.php">
