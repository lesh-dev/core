<?php
	@include("../settings.php");
?>
<html>
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>Нет такой страницы :: ФизЛЭШ</title>
</head>
<body>
	<style>
	    div.error-widget {
	        border: 1px solid #7f7f7f;
	        border-radius: 3px;
	        margin-top: 10px;
	        margin-bottom: 10px;
	        padding-left: 10px;
	        padding-right: 10px;
	        padding-bottom: 10px;
	        width: 600px;
	        background-color: #dddcae;
	    }
	    div.signature {
	    	font-style: italic;
	    	text-align: right;
	    }
	</style>

	<div class="error-widget">
		<h2>Нет такой страницы</h2>
		<p>
			Страница, которую Вы запросили, не существует!
			Возможно, это какая-то ошибка на нашем сайте, а может быть,
			Вам попалась устаревшая ссылка где-то на просторах Интернета.
		</p>
		<p>
			Пожалуйста, напишите об этой неприятности по адресу
			<a href="mailto:bug@fizlesh.ru"><tt>bug@fizlesh.ru</tt></a>
			и мы постараемся исправить эту проблему!
		</p>
		<p>
			В любом случае, не расстраивайтесь! Скорее всего, Вы
			найдёте нужную Вам информацию на нашем сайте.
			Пройдите по <a href="/<?php
				// even if web_prefix is empty, we still got a valid link
			    // to almost every production site root
				echo @$_web_prefix;
			?>">этой ссылке</a>,
			чтобы вернуться на сайт!
		</p>
		<div class="signature">С уважением, команда ФизЛЭШ</div>
	</div>
</body>
</html>