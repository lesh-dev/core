<?php
	function translit($rustring)
	{
		$rez = $rustring;

		$rez = str_replace("à","01r",$rez);
		$rez = str_replace("á","02r",$rez);
		$rez = str_replace("â","04r",$rez);
		$rez = str_replace("ã","05r",$rez);
		$rez = str_replace("ä","06r",$rez);
		$rez = str_replace("å","07r",$rez);
		$rez = str_replace("¸","08r",$rez);
		$rez = str_replace("æ","09r",$rez);
		$rez = str_replace("ç","10r",$rez);
		$rez = str_replace("è","11r",$rez);
		$rez = str_replace("é","12r",$rez);
		$rez = str_replace("ê","13r",$rez);
		$rez = str_replace("ë","14r",$rez);
		$rez = str_replace("ì","15r",$rez);
		$rez = str_replace("í","16r",$rez);
		$rez = str_replace("î","17r",$rez);
		$rez = str_replace("ï","18r",$rez);
		$rez = str_replace("ð","19r",$rez);
		$rez = str_replace("ñ","20r",$rez);
		$rez = str_replace("ò","21r",$rez);
		$rez = str_replace("ó","22r",$rez);
		$rez = str_replace("ô","23r",$rez);
		$rez = str_replace("õ","24r",$rez);
		$rez = str_replace("ö","25r",$rez);
		$rez = str_replace("÷","26r",$rez);
		$rez = str_replace("ø","27r",$rez);
		$rez = str_replace("ù","28r",$rez);
		$rez = str_replace("ú","29r",$rez);
		$rez = str_replace("û","30r",$rez);
		$rez = str_replace("ü","31r",$rez);
		$rez = str_replace("ý","32r",$rez);
		$rez = str_replace("þ","33r",$rez);
		$rez = str_replace("ÿ","34r",$rez);


		$rez = str_replace("À","01R",$rez);
		$rez = str_replace("Á","02R",$rez);
		$rez = str_replace("Â","04R",$rez);
		$rez = str_replace("Ã","05R",$rez);
		$rez = str_replace("Ä","06R",$rez);
		$rez = str_replace("Å","07R",$rez);
		$rez = str_replace("¨","08R",$rez);
		$rez = str_replace("Æ","09R",$rez);
		$rez = str_replace("Ç","10R",$rez);
		$rez = str_replace("È","11R",$rez);
		$rez = str_replace("¨","12R",$rez);
		$rez = str_replace("Ê","13R",$rez);
		$rez = str_replace("Ë","14R",$rez);
		$rez = str_replace("Ì","15R",$rez);
		$rez = str_replace("Í","16R",$rez);
		$rez = str_replace("Î","17R",$rez);
		$rez = str_replace("Ï","18R",$rez);
		$rez = str_replace("Ð","19R",$rez);
		$rez = str_replace("Ñ","20R",$rez);
		$rez = str_replace("Ò","21R",$rez);
		$rez = str_replace("Ó","22R",$rez);
		$rez = str_replace("Ô","23R",$rez);
		$rez = str_replace("Õ","24R",$rez);
		$rez = str_replace("Ö","25R",$rez);
		$rez = str_replace("×","26R",$rez);
		$rez = str_replace("Ø","27R",$rez);
		$rez = str_replace("Ù","28R",$rez);
		$rez = str_replace("Ú","29R",$rez);
		$rez = str_replace("Û","30R",$rez);
		$rez = str_replace("Ü","31R",$rez);
		$rez = str_replace("Ý","32R",$rez);
		$rez = str_replace("Þ","33R",$rez);
		$rez = str_replace("ß","34R",$rez);
		return $rez;
	}
	
	function database_replacer($text, $ELEMS, $primary, $method="view",$ELEMS_TYPES=array())
	{
  	global $pageid,$_POST,$_GET,$maxnum, $n_elems,$spt;
		$text = str_replace("{{search}}",'<input name="spt">',$text);
		$text = str_replace("{{sseq}}",@$spt,$text);
		
		if((@$_GET["show"]+$maxnum)<$n_elems)
		$text = str_replace("{{next}}", "href=\"?ref={$_GET["ref"]}&page=$pageid&show=".(@$_GET["show"]+$maxnum)."&spt=$spt\"",$text);
		else $text = str_replace("{{next}}","",$text);
		
		if((@$_GET["show"]-$maxnum)>=0)
		$text = str_replace("{{prev}}", "href=\"?ref={$_GET["ref"]}&page=$pageid&show=".(@$_GET["show"]-$maxnum)."&spt=$spt\"",$text);
		else $text = str_replace("{{prev}}","",$text);
		
		
		$text = str_replace("{{href}}","href=\"?ref={$_GET["ref"]}&page=$pageid&elem=$primary&spt=$spt\"",$text);
		$text = str_replace("{{ahref}}","href=\"?ref={$_GET["ref"]}&page=$pageid&elem=$primary&spt=$spt&mode=admin\"",$text);
		$text = str_replace("{{thref}}","?ref={$_GET["ref"]}&page=$pageid&elem=$primary&spt=$spt",$text);
		foreach($ELEMS as $k=>$v)
		{
           if($method=="view") $text = str_replace("{{".$k."}}",$v,$text);
      else if($method=="edit") $text = str_replace("{{".$k."}}","<input type=\"{$ELEMS_TYPES[$k]}\" name=\"$k\" value=\"$v\">",$text);
		}
    return $text;
	}	
?>
