function OnDocumentKeyPress(event) {
	var evt = (window.event ? window.event : event);
	var id;
	var sSubAction="";
	if (evt.ctrlKey && !evt.shiftKey && evt.keyCode == 13) {
		id = "btnQuickReplyPost";
	} else if (evt.ctrlKey && evt.shiftKey && evt.keyCode == 13) {
		id = "btnQuickReplyPreview";
		sSubAction="&preview=yes";
	}
	if (!id) return;
	var e = document.getElementById(id);
	var res = (e ? submitThisOnce(e) : null);
	var f = document.getElementById("postmodify");
	if (f) {
		f.action += sSubAction;
		f.submit();
	}
	return res;
}
document.onkeypress=OnDocumentKeyPress;