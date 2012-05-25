function CheckName(aError) {
  var val = $("#i-Name").val();
  val = $.trim(val);
  valLenTest = val.replace(/[^a-zA-Zа-яА-Я]/g, '');
  if (valLenTest.length < 4) {
    aError.push("Неправильно указано ФИО");
    return;
  }
  if (valLenTest.length > 80) {
    aError.push("Слишком длинное ФИО");
    return;
  }
  if (val.indexOf(' ') < 0) {
    aError.push("ФИО должно содержать хотя бы один пробел");
    return;
  }
}

function CheckClass(aError) {
  var val = $("#i-Class").val();
  val = $.trim(val);
  if (val.length < 1) aError.push("Класс не указан");
}

function CheckEMail(aError) {
  var val = $("#i-EMail").val();
  val = $.trim(val);
  if (val.length && val.indexOf('@') < 0) aError.push("EMail должен содержать знак '@'");
}

function CheckPhone(id, nDigit) {
  var val = $(id).val();
  val = $.trim(val);
  valLenTest = val.replace(/[^0-9]/g, '');
  if (valLenTest.length < nDigit) return "телефон должен содержать не меньше " + nDigit + " цифр. ";
  return '';
}

function CheckPhones(aError) {
  var sPhError = CheckPhone("#i-Phone", 7);
  var sCellError = CheckPhone("#i-Cellular", 9);
  if (sPhError.length && sCellError.length) aError.push("Укажите правильно хотя бы один из телефонов! Домашний "+sPhError + "Мобильный "+sCellError);
}

function CheckEmpty(id, sDesc, aResult) {
  var val = $(id).val();
  val = $.trim(val);
  if (val.length < 2) aResult.push("Вы не указали " + sDesc);
}

function WarnPersonal(aWarning) {
  CheckEmpty("#i-Favourites", "любимые предметы", aWarning);
  CheckEmpty("#i-Achivements", "достижения", aWarning);
  CheckEmpty("#i-Hobby", "хобби", aWarning);
}

function MakeList(aList) {
  var sRes = '<ul class="ankList">';
  for (var i = 0; i < aList.length; ++i) {
    sRes += ("<li>" + aList[i] + "</li>");
  }
  return sRes + "</ul>";
}

var GShowWarning = true;

$(document).ready(function() {

  $('#b-Submit').click(function() {  
    var aError = [];
    CheckName(aError);
    CheckClass(aError);
    CheckPhones(aError);
    CheckEMail(aError);
    
    var aWarning = [];
    WarnPersonal(aWarning);

    var bResult = true;
    if (aError.length) {
      $("#t-Error").html(MakeList(aError));
      bResult = false;
    } else {
      $("#t-Error").html(' ');
    }

    if (aWarning.length) {
      var sWarning = MakeList(aWarning);
      // warn once
      if (bResult) { // no severe errors detected
        $("#t-Warning").html(sWarning + "<p>Если Вы уверены, что не хотите указывать эту информацию, нажмите кнопку <b>Отправить</b> ещё раз.</p>");
        if (GShowWarning) { 
          GShowWarning = false;
          bResult = false;
        }
      } else {
        $("#t-Warning").html(sWarning);
        GShowWarning = true; // restore flag in case of severe errors
      }
    } else {
      $("#t-Warning").html(' ');
    }
    if (!aError.length && !aWarning.length) $("#c-Message").hide();
    else $("#c-Message").show();

    return bResult;
  });
});