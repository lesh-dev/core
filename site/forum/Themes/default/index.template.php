<?php
// Version: 1.1.5; index

/*	This template is, perhaps, the most important template in the theme. It
	contains the main template layer that displays the header and footer of
	the forum, namely with main_above and main_below. It also contains the
	menu sub template, which appropriately displays the menu; the init sub
	template, which is there to set the theme up; (init can be missing.) and
	the linktree sub template, which sorts out the link tree.

	The init sub template should load any data and set any hardcoded options.

	The main_above sub template is what is shown above the main content, and
	should contain anything that should be shown up there.

	The main_below sub template, conversely, is shown after the main content.
	It should probably contain the copyright statement and some other things.

	The linktree sub template should display the link tree, using the data
	in the $context['linktree'] variable.

	The menu sub template should display all the relevant buttons the user
	wants and or needs.

	For more information on the templating system, please see the site at:
	http://www.simplemachines.org/
*/

// Initialize the template... mainly little settings.
function template_init()
{
	global $context, $settings, $options, $txt;

	/* Use images from default theme when using templates from the default theme?
		if this is 'always', images from the default theme will be used.
		if this is 'defaults', images from the default theme will only be used with default templates.
		if this is 'never' or isn't set at all, images from the default theme will not be used. */
	$settings['use_default_images'] = 'never';

	/* What document type definition is being used? (for font size and other issues.)
		'xhtml' for an XHTML 1.0 document type definition.
		'html' for an HTML 4.01 document type definition. */
	$settings['doctype'] = 'xhtml';

	/* The version this template/theme is for.
		This should probably be the version of SMF it was created for. */
	$settings['theme_version'] = '1.1';

	/* Set a setting that tells the theme that it can render the tabs. */
	$settings['use_tabs'] = true;

	/* Use plain buttons - as oppossed to text buttons? */
	$settings['use_buttons'] = true;

	/* Show sticky and lock status seperate from topic icons? */
	$settings['seperate_sticky_lock'] = true;
}

// The main sub template above the content.
function template_main_above()
{
	global $context, $settings, $options, $scripturl, $txt, $modSettings;
	global $customSettings, $boardurl;
	global $PHP_SELF;

	// Show right to left and the character set for ease of translating.
	echo '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"', $context['right_to_left'] ? ' dir="rtl"' : '', '><head>
	<meta http-equiv="Content-Type" content="text/html; charset=', $context['character_set'], '" />
	<meta name="description" content="', $context['page_title'], '" />', empty($context['robot_no_index']) ? '' : '
	<meta name="robots" content="noindex" />', '
	<meta name="keywords" content="', $customSettings['PageKeywords'], '" />
	<script language="JavaScript" type="text/javascript" src="', $settings['default_theme_url'], '/script.js?fin11"></script>
	<script language="JavaScript" type="text/javascript" src="', $settings['default_theme_url'], '/index.js"></script>
	<script language="JavaScript" type="text/javascript"><!-- // --><![CDATA[
		var smf_theme_url = "', $settings['theme_url'], '";
		var smf_images_url = "', $settings['images_url'], '";
		var smf_scripturl = "', $scripturl, '";
		var smf_iso_case_folding = ', $context['server']['iso_case_folding'] ? 'true' : 'false', ';
		var smf_charset = "', $context['character_set'], '";
	// ]]></script>
	<title>', $context['page_title'], '</title>';

	// The ?fin11 part of this link is just here to make sure browsers don't cache it wrongly.
	echo '
	<link rel="stylesheet" type="text/css" href="', $settings['theme_url'], '/style.css?fin11" />
	<link rel="stylesheet" type="text/css" href="', $settings['default_theme_url'], '/print.css?fin11" media="print" />';

	/* Internet Explorer 4/5 and Opera 6 just don't do font sizes properly. (they are big...)
		Thus, in Internet Explorer 4, 5, and Opera 6 this will show fonts one size smaller than usual.
		Note that this is affected by whether IE 6 is in standards compliance mode.. if not, it will also be big.
		Standards compliance mode happens when you use xhtml... */
	if ($context['browser']['needs_size_fix'])
		echo '
	<link rel="stylesheet" type="text/css" href="', $settings['default_theme_url'], '/fonts-compat.css" />';

	// Show all the relative links, such as help, search, contents, and the like.
	echo '
	<link rel="help" href="', $scripturl, '?action=help" target="_blank" />
	<link rel="search" href="' . $scripturl . '?action=search" />
	<link rel="contents" href="', $scripturl, '" />';

	// If RSS feeds are enabled, advertise the presence of one.
	if (!empty($modSettings['xmlnews_enable']))
		echo '
	<link rel="alternate" type="application/rss+xml" title="', $context['forum_name'], ' - RSS" href="', $scripturl, '?type=rss;action=.xml" />';

	// If we're viewing a topic, these should be the previous and next topics, respectively.
	if (!empty($context['current_topic']))
		echo '
	<link rel="prev" href="', $scripturl, '?topic=', $context['current_topic'], '.0;prev_next=prev" />
	<link rel="next" href="', $scripturl, '?topic=', $context['current_topic'], '.0;prev_next=next" />';

	// If we're in a board, or a topic for that matter, the index will be the board's index.
	if (!empty($context['current_board']))
		echo '
	<link rel="index" href="' . $scripturl . '?board=' . $context['current_board'] . '.0" />';

	// We'll have to use the cookie to remember the header...
	if ($context['user']['is_guest'])
	{
		$options['collapse_header'] = !empty($_COOKIE['upshrink']);
		$options['collapse_header_ic'] = !empty($_COOKIE['upshrinkIC']);
	}

	// Output any remaining HTML headers. (from mods, maybe?)
	echo $context['html_headers'], '

	<script language="JavaScript" type="text/javascript"><!-- // --><![CDATA[
		var current_header = ', empty($options['collapse_header']) ? 'false' : 'true', ';
		var GUserLanguage = "', $context['user']['language'], '";

		function shrinkHeader(mode)
		{';

	// Guests don't have theme options!!
	if ($context['user']['is_guest'])
		echo '
			document.cookie = "upshrink=" + (mode ? 1 : 0);';
	else
		echo '
			smf_setThemeOption("collapse_header", mode ? 1 : 0, null, "', $context['session_id'], '");';

	echo '
			document.getElementById("upshrink").src = smf_images_url + (mode ? "/upshrink2.gif" : "/upshrink.gif");

			document.getElementById("upshrinkHeader").style.display = mode ? "none" : "";
			document.getElementById("upshrinkHeader2").style.display = mode ? "none" : "";

			current_header = mode;
		}
	// ]]></script>';

	// the routine for the info center upshrink
	echo '
		<script language="JavaScript" type="text/javascript"><!-- // --><![CDATA[
			var current_header_ic = ', empty($options['collapse_header_ic']) ? 'false' : 'true', ';

			function shrinkHeaderIC(mode)
			{';

	if ($context['user']['is_guest'])
		echo '
				document.cookie = "upshrinkIC=" + (mode ? 1 : 0);';
	else
		echo '
				smf_setThemeOption("collapse_header_ic", mode ? 1 : 0, null, "', $context['session_id'], '");';

	echo '
				document.getElementById("upshrink_ic").src = smf_images_url + (mode ? "/expand.gif" : "/collapse.gif");

				document.getElementById("upshrinkHeaderIC").style.display = mode ? "none" : "";

				current_header_ic = mode;
			}
		// ]]></script>
</head>
<body onload="InitializeButtons();">';
	echo '
	<div class="tborder" ', $context['browser']['needs_size_fix'] && !$context['browser']['is_ie6'] ? ' style="width: 100%;"' : '', '>
		<table width="100%" cellpadding="0" cellspacing="0" border="0">
			<tr>
				<td class="catbg" height="32" width="100%">';
	if (empty($settings['header_logo_url'])) {
		echo '<span class="forumHeaderTitle"><a href="'.$boardurl.'">'.$context['forum_name'].'</a></span>';
	} else {
		echo '<img src="', $settings['header_logo_url'], '" style="margin: 4px;" alt="', $context['forum_name'], '" />';
	}
	if($context['user']['is_logged']) {
		echo '<span class="userHello"> :: ', $txt['hello_member_ndt'], ' <b><a href="'.$boardurl.'/index.php?action=profile">'.
			$context['user']['name'].'</a></b></span>';
	}

	// display search panel
	// and the upshrink button for the user info section
	// TODO: reincarnate logo image
	echo '</td>
				<td align="right" class="catbg" style="white-space: nowrap;">
 					<!--<img src="', $settings['images_url'], '/smflogo.gif" style="margin: 2px;" alt="" />-->
					
					<span><form action="', $scripturl, '?action=search2" method="post" accept-charset="', $context['character_set'], '" style="margin: 0;">
						<a href="', $scripturl, '?action=search;advanced" style="vertical-align: bottom"><img src="'.$settings['images_url'].'/search-small.png" style="align: middle; margin: 0 .5ex;" alt="Advanced Search" title="Advanced Search"/></a>
						<input type="text" id="search" name="search" value="" style="width: 190px;" />&nbsp;';
						makeSubmit('Search', 100, $txt[182]);
						echo '<input type="hidden" name="advanced" value="0" />';
		
					// Search within current topic?
					if (!empty($context['current_topic'])) {
						echo '<input type="hidden" name="topic" value="', $context['current_topic'], '" />';
					} elseif (!empty($context['current_board'])) {
						// If we're on a certain board, limit it to this board ;).
						echo '<input type="hidden" name="brd[', $context['current_board'], ']" value="', $context['current_board'], '" />';
					}
					echo '</form></td><td class="catbg" style="padding-left:0px">
						<a href="#" onclick="shrinkHeader(!current_header); return false;"><img id="upshrink" src="', $settings['images_url'], '/', empty($options['collapse_header']) ? 'upshrink.gif' : 'upshrink2.gif', '" alt="*" title="', $txt['upshrink_description'], '" align="bottom" style="margin: 0 1ex;" /></a></td>
			</tr>
		</table>';
	echo "<script>ButtonCreate('Search', 'search');</script>";

	echo '
		<table width="100%" cellpadding="0" cellspacing="0" border="0" >
			<tr id="upshrinkHeader"', empty($options['collapse_header']) ? '' : ' style="display: none;"', '>
				<td valign="top" colspan="2">
					<table width="100%" class="bordercolor" cellpadding="8" cellspacing="1" border="0" style="margin-top: 1px;">
						<tr>';

	if (!empty($context['user']['avatar']))
		echo '
							<td class="windowbg" valign="middle">', $context['user']['avatar']['image'], '</td>';

	echo '
							<td colspan="2" width="100%" valign="top" class="windowbg2"><span class="middletext">';

	// If the user is logged in, display stuff like their name, new messages, etc.
	if ($context['user']['is_logged'])
	{
		echo '
								<a href="', $scripturl, '?action=unread">', $txt['unread_since_visit'], '</a> <br />
								<a href="', $scripturl, '?action=unreadreplies">', $txt['show_unread_replies'], '</a><br />';

	}
	// Otherwise they're a guest - send them a lovely greeting...
	else
		echo $txt['welcome_guest'];

	// Now, onto our second set of info, are they logged in again?
	if ($context['user']['is_logged'])
	{
		// Is the forum in maintenance mode?
		if ($context['in_maintenance'] && $context['user']['is_admin'])
			echo '
								<b>', $txt[616], '</b><br />';

		// Are there any members waiting for approval?
		if (!empty($context['unapproved_members']))
			echo '
								', $context['unapproved_members'] == 1 ? $txt['approve_thereis'] : $txt['approve_thereare'], ' <a href="', $scripturl, '?action=viewmembers;sa=browse;type=approve">', $context['unapproved_members'] == 1 ? $txt['approve_member'] : $context['unapproved_members'] . ' ' . $txt['approve_members'], '</a> ', $txt['approve_members_waiting'], '<br />';

		// Show the total time logged in?
		if (!empty($context['user']['total_time_logged_in']))
		{
			echo '
								', $txt['totalTimeLogged1'];

			// If days is just zero, don't bother to show it.
			if ($context['user']['total_time_logged_in']['days'] > 0)
				echo $context['user']['total_time_logged_in']['days'] . $txt['totalTimeLogged2'];

			// Same with hours - only show it if it's above zero.
			if ($context['user']['total_time_logged_in']['hours'] > 0)
				echo $context['user']['total_time_logged_in']['hours'] . $txt['totalTimeLogged3'];

			// But, let's always show minutes - Time wasted here: 0 minutes ;).
			echo $context['user']['total_time_logged_in']['minutes'], $txt['totalTimeLogged4'], '<br />';
		}
		echo '				</span>';
	}
	// Otherwise they're a guest - this time ask them to either register or login - lazy bums...
	else
	{
		echo '				</span>
								<script language="JavaScript" type="text/javascript" src="', $settings['default_theme_url'], '/sha1.js"></script>

								<form action="', $scripturl, '?action=login2" method="post" accept-charset="', $context['character_set'], '" class="middletext" style="margin: 3px 1ex 1px 0;"', empty($context['disable_login_hashing']) ? ' onsubmit="hashLoginPassword(this, \'' . $context['session_id'] . '\');"' : '', '>
									<input type="text" name="user" size="10" /> <input type="password" name="passwrd" size="10" />
									<select name="cookielength">
										<option value="60">', $txt['smf53'], '</option>
										<option value="1440">', $txt['smf47'], '</option>
										<option value="10080">', $txt['smf48'], '</option>
										<option value="43200">', $txt['smf49'], '</option>
										<option value="-1" selected="selected">', $txt['smf50'], '</option>
									</select>';
									makeSubmit('Login', 100, $txt[34]);
									echo '<br />
									<span class="middletext">', $txt['smf52'], '</span>
									<input type="hidden" name="hash_passwrd" value="" />
								</form>';
		echo '<script>ButtonCreate("Login", "login");</script>';
	}

	echo '
							</td>
						</tr>
					</table>
				</td>
			</tr>
		</table>';

	echo '
		<table id="upshrinkHeader2"', empty($options['collapse_header']) ? '' : ' style="display: none;"', ' width="100%" cellpadding="4" cellspacing="0" border="0">
			<tr>';

	// Show a random news item? (or you could pick one from news_lines...)
	if (!empty($settings['enable_news']))
		echo '
				<td width="90%" class="titlebg2">
					<span class="smalltext"><b>', $txt[102], '</b>: ', $context['random_news_line'], '</span>
				</td>';
	echo '
			</tr>
		</table>
	</div>';


	// Show the menu here, according to the menu sub template.
	template_menu();


	// The main content should go here.
	echo '
	<div id="bodyarea" style="padding: 1ex 0px 2ex 0px;">';
}

function template_main_below()
{
	global $context, $settings, $options, $scripturl, $txt;

	// Show the "Powered by" and "Valid" logos, as well as the copyright. Remember, the copyright must be somewhere!
	echo '
	<div style="display:none">',
 	theme_copyright(),
	'</div>
	<div id="footerarea" style="text-align: center; padding-bottom: 1ex;', $context['browser']['needs_size_fix'] && !$context['browser']['is_ie6'] ? ' width: 100%;' : '', '">',
	'<span class="smalltext copyright">',
	'Powered by <a href="http://www.simplemachines.org/" title="Simple Machines Forum" target="_blank">SMF 1.1.11</a>, &copy; 2006&#8211;2009.',
 	' Changes &amp; tweaks &copy; <a href="http://fizlesh.ru">fizlesh.ru</a> team, 2010 [Version '.trim(file_get_contents('version')).']',
	'</span>';

		// Show the load time?
	if ($context['show_load_time'])
		echo '
		<span class="smalltext">', $txt['smf301'], $context['load_time'], $txt['smf302'], $context['load_queries'], $txt['smf302b'], '</span>';

	// This is an interesting bug in Internet Explorer AND Safari. Rather annoying, it makes overflows just not tall enough.
	if (($context['browser']['is_ie'] && !$context['browser']['is_ie4']) ||
		$context['browser']['is_mac_ie'] ||
		$context['browser']['is_safari'] ||
		$context['browser']['is_firefox']) {
		// The purpose of this code is to fix the height of overflow: auto div blocks, because IE can't figure it out for itself.
		echo '<script language="JavaScript" type="text/javascript"><!-- // --><![CDATA[';
		// Unfortunately, Safari does not have a "getComputedStyle" implementation yet, so we have to just do it to code...
		if ($context['browser']['is_safari']) {
			echo 'var smf_codeFix=smf_codeFix_safari;';
			echo 'window.addEventListener("load", smf_codeFix, false);';
		} elseif ($context['browser']['is_firefox']) {
			echo 'var smf_codeFix=smf_codeFix_firefox;';
			echo 'window.addEventListener("load", smf_codeFix, false);';
		} else {
			echo 'var smf_codeFix=smf_codeFix_other;';
			echo 'var window_oldOnload = window.onload;';
			echo 'window.onload = smf_codeFix;';
		}
		echo '// ]]></script>';
	}

	echo '</div>';

	// The following will be used to let the user know that some AJAX process is running
	echo '
	<div id="ajax_in_progress" style="display: none;', $context['browser']['is_ie'] && !$context['browser']['is_ie7'] ? 'position: absolute;' : '', '">', $txt['ajax_in_progress'], '</div>
</body></html>';
}

// Show a linktree. This is that thing that shows "My Community | General Category | General Discussion"..
function theme_linktree()
{
	global $context, $settings, $options;

	echo '<div class="nav" style="font-size: smaller; margin-bottom: 2ex; margin-top: 2ex;">';

	// Each tree item has a URL and name. Some may have extra_before and extra_after.
	foreach ($context['linktree'] as $link_num => $tree)
	{
		// Show something before the link?
		if (isset($tree['extra_before']))
			echo $tree['extra_before'];

		// Show the link, including a URL if it should have one.
		echo '<b>', $settings['linktree_link'] && isset($tree['url']) ? '<a href="' . $tree['url'] . '" class="nav">' . $tree['name'] . '</a>' : $tree['name'], '</b>';

		// Show something after the link...?
		if (isset($tree['extra_after']))
			echo $tree['extra_after'];

		// Don't show a separator for the last one.
		if ($link_num != count($context['linktree']) - 1)
			echo '&nbsp;>&nbsp;';
	}

	echo '</div>';
}

function drawMainMenuButton($sAction, $sTitle, $current_action, $first, $last, $bPrevActive) {
	global $scripturl;
	global $context;
	$sSessionSpike = ($sAction == 'logout') ? ';sesc='.$context['session_id'] : '';
	$bActive = ($current_action == $sAction);
	if (!$bPrevActive && !$bActive) echo '<td class="maintab_sep">|</td>';
	echo ($bActive || $context['browser']['is_ie4']) ?
		'<td class="maintab_active_' . $first . '">&nbsp;</td>' : '' ,
		'<td valign="top" class="maintab_' , ($bActive ? 'active_back' : 'back') , '">';
	
	echo '<a href="', $scripturl, '?action=', $sAction.$sSessionSpike, '">', $sTitle, '</a>
		</td>' , ($bActive ? '<td class="maintab_active_'.$last.'">&nbsp;</td>' : '');
	return $bActive;
}

// Show the menu up top. Something like [home] [help] [profile] [logout]...
function template_menu()
{
	global $context, $settings, $options, $scripturl, $txt;

	// Work out where we currently are.
	$current_action = 'home';
	if (in_array($context['current_action'], array('admin', 'ban', 'boardrecount', 'cleanperms', 'detailedversion', 'dumpdb', 'featuresettings', 'featuresettings2', 'findmember', 'maintain', 'manageattachments', 'manageboards', 'managecalendar', 'managesearch', 'membergroups', 'modlog', 'news', 'optimizetables', 'packageget', 'packages', 'permissions', 'pgdownload', 'postsettings', 'regcenter', 'repairboards', 'reports', 'serversettings', 'serversettings2', 'smileys', 'viewErrorLog', 'viewmembers')))
		$current_action = 'admin';
	if (in_array($context['current_action'], array('search', 'admin', 'calendar', 'profile', 'mlist', 'register', 'login', 'help', 'pm')))
		$current_action = $context['current_action'];
	if ($context['current_action'] == 'search2')
		$current_action = 'search';
	if ($context['current_action'] == 'theme')
		$current_action = isset($_REQUEST['sa']) && $_REQUEST['sa'] == 'pick' ? 'profile' : 'admin';

	// Are we using right-to-left orientation?
	if ($context['right_to_left']) {
		$first = 'last';
		$last = 'first';
	} else {
		$first = 'first';
		$last = 'last';
	}

	// Show the start of the tab section.
	echo '
			<table cellpadding="0" cellspacing="0" border="0" style="margin-left: 10px;">
				<tr>
					<td class="maintab_' , $first , '">&nbsp;</td>';
	$bActive = true;
	$bActive = drawMainMenuButton('home', $txt[103], $current_action, $first, $last, $bActive);
	$bActive = drawMainMenuButton('help', $txt[119], $current_action, $first, $last, $bActive);
	if ($context['allow_search']) $bActive = drawMainMenuButton('search', $txt[182], $current_action, $first, $last, $bActive);
	if ($context['allow_admin']) $bActive = drawMainMenuButton('admin', $txt[2], $current_action, $first, $last, $bActive);
	if ($context['allow_edit_profile']) $bActive = drawMainMenuButton('profile', $txt[79], $current_action, $first, $last, $bActive);
	if ($context['user']['is_logged'] && $context['allow_pm']) {
		$sUnread = $context['user']['unread_messages'] > 0 ? ' [<strong>'. $context['user']['unread_messages'].'</strong>]' : '';
		$bActive = drawMainMenuButton('pm', $txt['pm_short'].$sUnread, $current_action, $first, $last, $bActive);
	}
	if ($context['allow_calendar']) $bActive = drawMainMenuButton('calendar', $txt['calendar24'], $current_action, $first, $last, $bActive);
	if ($context['allow_memberlist']) $bActive = drawMainMenuButton('mlist', $txt[331], $current_action, $first, $last, $bActive);
	if ($context['user']['is_guest']) {
		$bActive = drawMainMenuButton('login', $txt[34], $current_action, $first, $last, $bActive);
		$bActive = drawMainMenuButton('register', $txt[97], $current_action, $first, $last, $bActive);
	}
	if ($context['user']['is_logged']) $bActive = drawMainMenuButton('logout', $txt[108], $current_action, $first, $last, $bActive);
	// The end of tab section.
	echo '
				<td class="maintab_' , $last , '">&nbsp;</td>
			</tr>
		</table>';
}

// Generate a strip of buttons.
function template_button_strip($button_strip, $direction = 'top', $force_reset = false, $custom_td = '')
{
	global $settings, $buttons, $context, $txt, $scripturl;

	// Create the buttons...
	foreach ($button_strip as $key => $value)
	{
		if (isset($value['test']) && empty($context[$value['test']]))
		{
			unset($button_strip[$key]);
			continue;
		}
		elseif (!isset($buttons[$key]) || $force_reset)
			$buttons[$key] = '<a href="' . $value['url'] . '" ' .( isset($value['custom']) ? $value['custom'] : '') . '>' . $txt[$value['text']] . '</a>';

		$button_strip[$key] = $buttons[$key];
	}

	if (empty($button_strip))
		return '<td>&nbsp;</td>';

	echo '
		<td class="', $direction == 'top' ? 'main' : 'mirror', 'tab_' , $context['right_to_left'] ? 'last' : 'first' , '">&nbsp;</td>
		<td class="', $direction == 'top' ? 'main' : 'mirror', 'tab_back">', implode(' &nbsp;|&nbsp; ', $button_strip) , '</td>
		<td class="', $direction == 'top' ? 'main' : 'mirror', 'tab_' , $context['right_to_left'] ? 'first' : 'last' , '">&nbsp;</td>';
}

function makeSubmit($sID, $nWidth, $sTitle, $sOnClick='', $sExtra='') {
	echo "<span class=\"buttonBox w$nWidth\"><span id=\"span$sID\" class=\"buttonSelected w$nWidth\">&nbsp;</span><input
		type=\"submit\" value=\"\" alt=\"$sTitle\" title=\"$sTitle\" onclick=\"$sOnClick\"
		id=\"btn$sID\" class=\"coloredButton w$nWidth\" $sExtra/></span>";
}
?>
