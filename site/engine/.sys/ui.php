<?php
	function translit($rustring)
	{
		$rez = $rustring;

		$rez = str_replace("�","01r",$rez);
		$rez = str_replace("�","02r",$rez);
		$rez = str_replace("�","04r",$rez);
		$rez = str_replace("�","05r",$rez);
		$rez = str_replace("�","06r",$rez);
		$rez = str_replace("�","07r",$rez);
		$rez = str_replace("�","08r",$rez);
		$rez = str_replace("�","09r",$rez);
		$rez = str_replace("�","10r",$rez);
		$rez = str_replace("�","11r",$rez);
		$rez = str_replace("�","12r",$rez);
		$rez = str_replace("�","13r",$rez);
		$rez = str_replace("�","14r",$rez);
		$rez = str_replace("�","15r",$rez);
		$rez = str_replace("�","16r",$rez);
		$rez = str_replace("�","17r",$rez);
		$rez = str_replace("�","18r",$rez);
		$rez = str_replace("�","19r",$rez);
		$rez = str_replace("�","20r",$rez);
		$rez = str_replace("�","21r",$rez);
		$rez = str_replace("�","22r",$rez);
		$rez = str_replace("�","23r",$rez);
		$rez = str_replace("�","24r",$rez);
		$rez = str_replace("�","25r",$rez);
		$rez = str_replace("�","26r",$rez);
		$rez = str_replace("�","27r",$rez);
		$rez = str_replace("�","28r",$rez);
		$rez = str_replace("�","29r",$rez);
		$rez = str_replace("�","30r",$rez);
		$rez = str_replace("�","31r",$rez);
		$rez = str_replace("�","32r",$rez);
		$rez = str_replace("�","33r",$rez);
		$rez = str_replace("�","34r",$rez);


		$rez = str_replace("�","01R",$rez);
		$rez = str_replace("�","02R",$rez);
		$rez = str_replace("�","04R",$rez);
		$rez = str_replace("�","05R",$rez);
		$rez = str_replace("�","06R",$rez);
		$rez = str_replace("�","07R",$rez);
		$rez = str_replace("�","08R",$rez);
		$rez = str_replace("�","09R",$rez);
		$rez = str_replace("�","10R",$rez);
		$rez = str_replace("�","11R",$rez);
		$rez = str_replace("�","12R",$rez);
		$rez = str_replace("�","13R",$rez);
		$rez = str_replace("�","14R",$rez);
		$rez = str_replace("�","15R",$rez);
		$rez = str_replace("�","16R",$rez);
		$rez = str_replace("�","17R",$rez);
		$rez = str_replace("�","18R",$rez);
		$rez = str_replace("�","19R",$rez);
		$rez = str_replace("�","20R",$rez);
		$rez = str_replace("�","21R",$rez);
		$rez = str_replace("�","22R",$rez);
		$rez = str_replace("�","23R",$rez);
		$rez = str_replace("�","24R",$rez);
		$rez = str_replace("�","25R",$rez);
		$rez = str_replace("�","26R",$rez);
		$rez = str_replace("�","27R",$rez);
		$rez = str_replace("�","28R",$rez);
		$rez = str_replace("�","29R",$rez);
		$rez = str_replace("�","30R",$rez);
		$rez = str_replace("�","31R",$rez);
		$rez = str_replace("�","32R",$rez);
		$rez = str_replace("�","33R",$rez);
		$rez = str_replace("�","34R",$rez);
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
