/*
// 2005-03-21
// Copyright (c) Art. Lebedev | http://www.artlebedev.ru/
// Author - Vladimir Tokmakov
*/



function Make_Tabsheet(){
	var i, j, k, eDD, iMax_height, iDT_height, aeDL_child, sDD_inner_HTML
	var bFirst_tab = true
	var aeDl = document.getElementsByTagName( "DL" )

	for( i = 0 ; i < aeDl.length ; i++ ){
		if( aeDl[i].className == "tabsheets"  ){ // если у нас отработал CSS, то меняем высоту у tabsheet-ов
			aeDL_child = aeDl[i].childNodes
			iMax_height = 0
			for( j = 0 ; j < aeDL_child.length ; j++ ){
				if( aeDL_child[j].nodeName == "DT" ){
					iDT_height = aeDL_child[j].offsetHeight
					aeDL_child[j].unselectable = true
					aeDL_child[j].onmousedown = Switch_sheet
					eDD = aeDL_child[j]
					while( eDD.nextSibling ){
						eDD = eDD.nextSibling
						if( eDD.nodeName == "DD" ){
							if( eDD.offsetHeight > iMax_height ){
								iMax_height = eDD.offsetHeight
							}
							if( !bFirst_tab ){
								eDD.className = "inactive"
							}else{
								aeDL_child[j].className = "active"
							}
							bFirst_tab = false
							break
						}
					}
				}
			}
			aeDl[i].style.height = (iMax_height + iDT_height) * 1 + "px"
			for( j = 0 ; j < aeDL_child.length ; j++ ){
				if( aeDL_child[j].nodeName == "DD" ){
					aeDL_child[j].style.height = iMax_height + "px"
				}
			}
		}
		return true
	}
}

function Switch_sheet( e ){
	var eTab = e ? e.target : window.event.srcElement
	if( eTab.nodeType == 3){
		eTab = eTab.parentNode
	}
	var eSheet = eTab
	while( eSheet.nextSibling ){
		eSheet = eSheet.nextSibling
		if( eSheet.nodeName == "DD" ){
			break
		}
	}

	if( eSheet.className == "inactive" ){
		eTab.className = "on" 
		var aeDL_child = eTab.parentNode.childNodes
		for( var i = 0 ; i < aeDL_child.length ; i++ ){
			if( aeDL_child[i].nodeName == "DT" && aeDL_child[i].className != "on" ){
				aeDL_child[i].className = ""
			}else if( aeDL_child[i].nodeName == "DD" ){
				aeDL_child[i].className = "inactive"
			}
		}
		eSheet.className = "active"
		eTab.className = "active"
	}
	return false
}


