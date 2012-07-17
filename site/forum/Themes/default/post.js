// The actual message icon selector
function showimage() {
	document.images.icons.src = icon_urls[document.forms.postmodify.icon.options[document.forms.postmodify.icon.selectedIndex].value];
}

function previewPost() {
	if (window.XMLHttpRequest) {
		if (GIsFirefox) {
			// Firefox doesn't render <marquee> that have been put it using javascript
			if (document.forms.postmodify.elements["message"].value.indexOf("[move]") != -1)
			{
				return submitThisOnce(document.forms.postmodify);
			}
		}
		// Opera didn't support setRequestHeader() before 8.01.
		if (typeof(window.opera) != "undefined")
		{
			var test = new XMLHttpRequest();
			if (typeof(test.setRequestHeader) != "function")
				return submitThisOnce(document.forms.postmodify);
		}
		// !!! Currently not sending poll options and option checkboxes.
		var i, x = new Array();
		var textFields = ["subject", "message", "icon", "guestname", "email", "evtitle", "question", "topic"];
		var numericFields = [
			"board", "topic", "num_replies",
			"eventid", "calendar", "year", "month", "day",
			"poll_max_votes", "poll_expire", "poll_change_vote", "poll_hide"
		];
		var checkboxFields = [
			"ns"
		];

		for (i in textFields)
			if (document.forms.postmodify.elements[textFields[i]])
				x[x.length] = textFields[i] + "=" + escape(textToEntities(document.forms.postmodify[textFields[i]].value.replace(/&#/g, "&#38;#"))).replace(/\+/g, "%2B");
		for (i in numericFields)
			if (document.forms.postmodify.elements[numericFields[i]] && typeof(document.forms.postmodify[numericFields[i]].value) != "undefined")
				x[x.length] = numericFields[i] + "=" + parseInt(document.forms.postmodify.elements[numericFields[i]].value);
		for (i in checkboxFields)
			if (document.forms.postmodify.elements[checkboxFields[i]] && document.forms.postmodify.elements[checkboxFields[i]].checked)
				x[x.length] = checkboxFields[i] + "=" + document.forms.postmodify.elements[checkboxFields[i]].value;

		sendXMLDocument(smf_scripturl + "?action=post2" + (current_board ? ";board=" + current_board : "") + (make_poll ? ";poll" : "") + ";preview;xml", x.join("&"), onDocSent);

		document.getElementById("preview_section").style.display = "";
		setInnerHTML(document.getElementById("preview_subject"), txt_preview_title);
		setInnerHTML(document.getElementById("preview_body"), txt_preview_fetch);

		return false;
	}
	else
		return submitThisOnce(document.forms.postmodify);
}

function onDocSent(XMLDoc) {
	if (!XMLDoc) {
		document.forms.postmodify.preview.onclick = new function() { return true; }
		document.forms.postmodify.preview.click();
	}

	// Show the preview section
	var i, preview = XMLDoc.getElementsByTagName("smf")[0].getElementsByTagName("preview")[0];
	setInnerHTML(document.getElementById("preview_subject"), preview.getElementsByTagName("subject")[0].firstChild.nodeValue);

	var bodyText = "";
	for (i = 0; i < preview.getElementsByTagName("body")[0].childNodes.length; i++)
		bodyText += preview.getElementsByTagName("body")[0].childNodes[i].nodeValue;

	setInnerHTML(document.getElementById("preview_body"), bodyText);
	document.getElementById("preview_body").className = "post";

	// Show a list of errors (if any).
	var errors = XMLDoc.getElementsByTagName("smf")[0].getElementsByTagName("errors")[0];
	var numErrors = errors.getElementsByTagName("error").length, errorList = new Array();
	for (i = 0; i < numErrors; i++)
		errorList[errorList.length] = errors.getElementsByTagName("error")[i].firstChild.nodeValue;
	document.getElementById("errors").style.display = numErrors == 0 ? "none" : "";
	document.getElementById("error_serious").style.display = errors.getAttribute("serious") == 1 ? "" : "none";
	setInnerHTML(document.getElementById("error_list"), numErrors == 0 ? "" : errorList.join("<br />"));

	// Show a warning if the topic has been locked.
	document.getElementById("lock_warning").style.display = errors.getAttribute("topic_locked") == 1 ? "" : "none";

	// Adjust the color of captions if the given data is erroneous.
	var captions = errors.getElementsByTagName("caption"), numCaptions = errors.getElementsByTagName("caption").length;
	for (i = 0; i < numCaptions; i++)
		if (document.getElementById("caption_" + captions[i].getAttribute("name")))
			document.getElementById("caption_" + captions[i].getAttribute("name")).style.color = captions[i].getAttribute("color");

	if (errors.getElementsByTagName("post_error").length == 1)
		document.forms.postmodify.message.style.border = "1px solid red";
	else if (document.forms.postmodify.message.style.borderColor == "red" || document.forms.postmodify.message.style.borderColor == "red red red red")
	{
		if (typeof(document.forms.postmodify.message.runtimeStyle) == "undefined")
			document.forms.postmodify.message.style.border = null;
		else
			document.forms.postmodify.message.style.borderColor = "";
	}

	// Set the new number of replies.
	if (document.forms.postmodify.elements["num_replies"])
		document.forms.postmodify.num_replies.value = XMLDoc.getElementsByTagName("smf")[0].getElementsByTagName("num_replies")[0].firstChild.nodeValue;

	var newPosts = XMLDoc.getElementsByTagName("smf")[0].getElementsByTagName("new_posts")[0] ? XMLDoc.getElementsByTagName("smf")[0].getElementsByTagName("new_posts")[0].getElementsByTagName("post") : {length: 0};
	var numNewPosts = newPosts.length;
	if (numNewPosts != 0)
	{
		var newTable = '<span id="new_replies"></span><table width="100%" class="windowbg" cellspacing="0" cellpadding="2" align="center" style="table-layout: fixed;">';
		for (i = 0; i < numNewPosts; i++)
			newTable += '<tr class="catbg"><td colspan="2" align="left" class="smalltext"><div style="float: right;">'+GTxt280+': '+
				newPosts[i].getElementsByTagName("time")[0].firstChild.nodeValue +
				' <img src="' + smf_images_url + '/' + GUserLanguage + '/new.gif" alt="' + GTxtPreviewNew + '" /></div>'+GTxt279+': ' +
				newPosts[i].getElementsByTagName("poster")[0].firstChild.nodeValue + '</td></tr><tr class="windowbg2"><td colspan="2" class="smalltext" id="msg' +
				newPosts[i].getAttribute("id") + '" width="100%"><div align="right" class="smalltext"><a href="#top" onclick="return insertQuoteFast(\'' +
				newPosts[i].getAttribute("id") + '\');">'+GTxt260+'</a></div><div class="post">' +
				newPosts[i].getElementsByTagName("message")[0].firstChild.nodeValue + '</div></td></tr>';
		newTable += '</table>';
		setOuterHTML(document.getElementById("new_replies"), newTable);
	}

	if (typeof(smf_codeFix) != "undefined") smf_codeFix();
}

// A function needed to discern HTML entities from non-western characters
function saveEntities() {
	var textFields = ["subject", "message", "guestname", "evtitle", "question"];
	for (i in textFields) {
		if (document.forms.postmodify.elements[textFields[i]]) {
			document.forms.postmodify[textFields[i]].value = document.forms.postmodify[textFields[i]].value.replace(/&#/g, "&#38;#");
		}
	}
	for (var i = document.forms.postmodify.elements.length - 1; i >= 0; i--) {
		if (document.forms.postmodify.elements[i].name.indexOf("options") == 0) {
			document.forms.postmodify.elements[i].value = document.forms.postmodify.elements[i].value.replace(/&#/g, "&#38;#");
		}
	}
}

function swapOptions() {
	document.getElementById("postMoreExpand").src = smf_images_url + "/" + (currentSwap ? "collapse.gif" : "expand.gif");
	document.getElementById("postMoreExpand").alt = currentSwap ? "-" : "+";
	document.getElementById("postMoreOptions").style.display = currentSwap ? "" : "none";

	if (document.getElementById("postAttachment")) {
		document.getElementById("postAttachment").style.display = currentSwap ? "" : "none";
	}
	if (document.getElementById("postAttachment2")) {
		document.getElementById("postAttachment2").style.display = currentSwap ? "" : "none";
	}

	if (typeof(document.forms.postmodify) != "undefined") {
		document.forms.postmodify.additional_options.value = currentSwap ? "1" : "0";
	}
	currentSwap = !currentSwap;
}

function pollOptions() {
	var expireTime = document.getElementById("poll_expire");
	if (isEmptyText(expireTime) || expireTime.value == 0) {
		document.forms.postmodify.poll_hide[2].disabled = true;
		if (document.forms.postmodify.poll_hide[2].checked) {
			document.forms.postmodify.poll_hide[1].checked = true;
		}
	} else {
		document.forms.postmodify.poll_hide[2].disabled = false;
	}
}

function addPollOption() {
	if (pollOptionNum == 0) {
		for (var i = 0; i < document.forms.postmodify.elements.length; i++) {
			if (document.forms.postmodify.elements[i].id.substr(0, 8) == "options-") {
				pollOptionNum++;
				pollTabIndex = document.forms.postmodify.elements[i].tabIndex;
			}
		}
	}
	pollOptionNum++;
	setOuterHTML(document.getElementById("pollMoreOptions"), '<br /><label for="options-' + pollOptionNum + '">' + GTxtSMF22 + ' ' + pollOptionNum +
		'</label>: <input type="text" name="options[' + pollOptionNum + ']" id="options-' + pollOptionNum +
		'" value="" size="25" tabindex="' + pollTabIndex + '" /><span id="pollMoreOptions"></span>');
}

function generateDays() {
	var dayElement = document.getElementById("day"), yearElement = document.getElementById("year"), monthElement = document.getElementById("month");
	var days, selected = dayElement.selectedIndex;

	monthLength[1] = yearElement.options[yearElement.selectedIndex].value % 4 == 0 ? 29 : 28;
	days = monthLength[monthElement.value - 1];

	while (dayElement.options.length) dayElement.options[0] = null;

	for (i = 1; i <= days; i++) {
		dayElement.options[dayElement.length] = new Option(i, i);
	}

	if (selected < days) dayElement.selectedIndex = selected;
}

