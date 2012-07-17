function smf_codeFix_safari()
{
	var codeFix = document.getElementsByTagName ? document.getElementsByTagName("div") : document.all.tags("div");

	for (var i = 0; i < codeFix.length; i++) {
		if ((codeFix[i].className == "code" || codeFix[i].className == "post" ||
			codeFix[i].className == "signature") && codeFix[i].offsetHeight < 20) {
			codeFix[i].style.height = (codeFix[i].offsetHeight + 20) + "px";
		}
	}
}

function smf_codeFix_firefox()
{
	var codeFix = document.getElementsByTagName ? document.getElementsByTagName("div") : document.all.tags("div");
	for (var i = 0; i < codeFix.length; i++) {
		if (codeFix[i].className == "code" && (codeFix[i].scrollWidth > codeFix[i].clientWidth || codeFix[i].clientWidth == 0)) {
			codeFix[i].style.overflow = "scroll";
		}
	}
}

function smf_codeFix_other()
{
	var codeFix = document.getElementsByTagName ? document.getElementsByTagName("div") : document.all.tags("div");

	for (var i = codeFix.length - 1; i > 0; i--) {
		if (codeFix[i].currentStyle.overflow == "auto" &&
			(codeFix[i].currentStyle.height == "" || codeFix[i].currentStyle.height == "auto") &&
			(codeFix[i].scrollWidth > codeFix[i].clientWidth || codeFix[i].clientWidth == 0) &&
			(codeFix[i].offsetHeight != 0 || codeFix[i].className == "code")) {
			codeFix[i].style.height = (codeFix[i].offsetHeight + 36) + "px";
		}
	}

	if (window_oldOnload) {
		window_oldOnload();
		window_oldOnload = null;
	}
}


var aButtons = {};

function ButtonCreate(id, sImg) {
	aButtons[id]=sImg;
}

function InitializeButtons() {
	if (!aButtons) return;
	for (var id in aButtons) {
		var ele = document.getElementById('btn'+id);
		if (!ele) continue;
		var sImg=aButtons[id];
		ele.coloredID=id;
		
		ele.urlActive=smf_images_url+'/'+GUserLanguage+'/buttons/'+sImg+'-on.png';
		ele.urlPassive=smf_images_url+'/'+GUserLanguage+'/buttons/'+sImg+'-off.png';
		
		ele.onmousedown=ButtonOnMouseDown;
		ele.onmouseup=ButtonOnMouseUp;
		ele.style.backgroundImage = "url('"+ele.urlPassive+"')";
		
		var eS=document.getElementById('span'+id);
		if (!eS) continue;
		eS.style.backgroundImage="url('"+ele.urlActive+"')";
	}
}

function ButtonOnMouseDown() {
	if (!this.urlActive) return;
	var eS = document.getElementById('span'+this.coloredID);
	if (!eS) return;
	eS.style.visibility='visible';

	document.unclickButton=this;
	document.onmouseup=DocumentOnMouseUp;
}

function DocumentOnMouseUp() {
	if (!document.unclickButton) return;
	var oB=document.unclickButton;
	if (!oB || !oB.urlPassive) return;
	var eS = document.getElementById('span'+oB.coloredID);
	if (!eS) return;
	eS.style.visibility='hidden';
	document.unclickButton=undefined;
	document.onmouseup=null;
	oB.click();
}

function ButtonOnMouseUp() {
	if (!this.urlPassive) return;
	var eS = document.getElementById('span'+this.coloredID);
	if (!eS) return;
	eS.style.visibility='hidden';
}

