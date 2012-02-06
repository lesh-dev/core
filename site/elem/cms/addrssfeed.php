<?
  function addrssfeed($basetitle,$description,$link,$author)
  {
      global $SETTINGS, $pageid, $login, $INFO;
      $f = fopen("data/cms/rss/".mktime().".rss","w");
      fputs($f,"<item>\n");
      fputs($f,"<title>$basetitle: ".$INFO["header"]."</title>\n");
      if (empty($author))
        fputs($f,"<author>$login</author>\n");
      else
        fputs($f,"<author>$author</author>\n");
      if (empty($link))
        fputs($f,"<link>http://fizlesh.ru/?page=$pageid</link>\n");
      else
        fputs($f,"<link>$link</link>\n");
      fputs($f,"<guid>$pageid@".mktime()."</guid>\n");
      fputs($f,"<pubDate>".date("r")."</pubDate>\n");
      fputs($f,"<description>\n");
      fputs($f,$description."\n");
      fputs($f,"</description>\n");
      fputs($f,"</item>\n");
      fclose($f);
      $f = fopen("data/cms/rss/pubdate","w");
      fputs($f,"<pubDate>".date("r")."</pubDate>\n");
      fclose($f);
  }
?>
