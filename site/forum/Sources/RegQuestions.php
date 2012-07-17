<?php
	if (!defined('SMF')) die('Hacking attempt...');

	global $aRegQuestions, $aRegAnswers;
	$aRegQuestions = array();
	$aRegAnswers = array();
	
	// Array indexes must match questions and answers
	$aRegQuestions[0] = 'Физическая величина, выражаемая в Ньютонах:';
	$aRegQuestions[1] = 'Сколько букв в аббревиатуре &laquo;ЛЭШ&raquo;?';
	$aRegQuestions[2] = 'Число, не являющееся ни положительным, ни отрицательным:';

	$aRegAnswers[0] = array('сила', 'force');
	$aRegAnswers[1] = array('3', 'три', 'three');
	$aRegAnswers[2] = array('ноль', 'нуль');

?>
