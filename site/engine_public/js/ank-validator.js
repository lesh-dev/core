function CheckName(aError, sFieldName, sFieldTitle) {
    var val = $("#"+sFieldName+"-input").val();
    val = $.trim(val);
    valLenTest = val.replace(/[^a-zA-Zа-яА-Я]/g, '');
    if (valLenTest.length < 2) {
        aError.push("Поле '" + sFieldTitle + "' слишком короткое");
        return;
    }
    if (valLenTest.length > 80) {
        aError.push("Поле '" + sFieldTitle + "' слишком длинное");
        return;
    }
    if (/[\/.,?!@#$%&*()_+=~^]/.test(val)) {
        aError.push("Поле '" + sFieldTitle + "' должно содержать только русские и английские символы");
        return;
    }
}

function OnChange() {
    GShowWarning = true;
}

function CheckClass(aError) {
    var val = $("#current_class-input").val();
    val = $.trim(val);
    if (val.length < 1) aError.push("Класс не указан");
}

function CheckEMail(aError) {
    var val = $("#email-input").val();
    val = $.trim(val);
    if (val.length && val.indexOf('@') < 0)
        aError.push("EMail должен содержать знак '@'");
}

function CheckControlQuestion(aError) {
    var val = $("#control_question-input").val();
    val = $.trim(val);
    if (!(
        val.indexOf("ампер") >= 0 ||
        val.indexOf("Ампер") >= 0 ||
        val == "А" ||  // rus
        val == "а" ||  // rus
        val == "A" ||  // eng
        val == "a"  // eng
    )) {
        aError.push("Неправильный ответ на контрольный вопрос. Вспомните физику!");
    }
}

function CheckPhone(id, nDigit) {
    var val = $(id).val();
    val = $.trim(val);
    valLenTest = val.replace(/[^0-9]/g, '');
    if (valLenTest.length < nDigit)
        return "телефон должен содержать не меньше " + nDigit + " цифр. ";
    return '';
}

function CheckPhones(aError) {
    var sPhError = CheckPhone("#phone-input", 7);
    var sCellError = CheckPhone("#cellular-input", 9);
    if (sPhError.length && sCellError.length)
        aError.push("Укажите правильно хотя бы один из телефонов! Домашний " +
            sPhError + "Мобильный " + sCellError);
}

function CheckEmpty(id, sDesc, aResult) {
    var val = $(id).val();
    val = $.trim(val);
    if (val.length < 2)
        aResult.push("Вы не указали " + sDesc);
}

function WarnPersonal(aWarning) {
    CheckEmpty("#favourites-text", "любимые предметы", aWarning);
    CheckEmpty("#achievements-text", "достижения", aWarning);
    CheckEmpty("#hobby-text", "хобби", aWarning);
    //CheckEmpty("#lesh_ref-text", "откуда Вы узнали о школе", aWarning);
}

function MakeList(aList) {
    var sRes = '<ul class="ankMessageList">';
    for (var i = 0; i < aList.length; ++i)
        sRes += ("<li>" + aList[i] + "</li>");
    return sRes + "</ul>";
}

var GShowWarning = true;

$(document).ready(function() {

    $('#favourites-text').change(OnChange);
    $('#achievements-text').change(OnChange);
    $('#hobby-text').change(OnChange);

    $('#submit-anketa-button').click(function() {
        var aError = [];
        CheckName(aError, 'last_name', 'Фамилия');
        CheckName(aError, 'first_name', 'Имя');
        CheckName(aError, 'patronymic', 'Отчество');
        CheckClass(aError);
        CheckPhones(aError);
        CheckEMail(aError);
        CheckControlQuestion(aError);

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
                $("#t-Warning").html(sWarning +
                    "<p>Если Вы уверены, что не хотите указывать эту информацию, нажмите кнопку <b>Отправить</b> ещё раз.</p>");
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
