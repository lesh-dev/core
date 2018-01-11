function xsm_ank_check_name(aError, sFieldName, sFieldTitle) {
    var val = $("#" + sFieldName + "-input").val();
    val = $.trim(val);
    var valLenTest = val.replace(/[^a-zA-Zа-яА-Я]/g, '');
    if (valLenTest.length < 2) {
        aError.push("Поле '" + sFieldTitle + "' слишком короткое");
        return false;
    }
    if (valLenTest.length > 80) {
        aError.push("Поле '" + sFieldTitle + "' слишком длинное");
        return false;
    }
    if (/[\/.,?!@#$%&*()_+=~^]/.test(val)) {
        aError.push("Поле '" + sFieldTitle + "' должно содержать только русские и английские символы");
        return false;
    }
    return true;
}

function xsm_ank_on_change() {
    GShowWarning = true;
}

function xsm_ank_check_class(aError) {
    var val = $("#ank_class-input").val();
    val = $.trim(val);
    if (val.length < 1) aError.push("Класс не указан");
}

function xsm_ank_check_birth_date(aError, sFieldName, sFieldTitle) {
    var val = $("#" + sFieldName + "-input").val();
    val = $.trim(val);
    if (!/\d\d.\d\d.\d\d\d\d/.test(val)) {
        aError.push("Поле '" + sFieldTitle + "' должно иметь формат ДД.ММ.ГГГГ");
        return false;
    }
    return true;
}

/**
 * @param errors: array of errors to push new errors
 * @param element_name: non-default element name to check
 */
function xsm_ank_check_email(errors, element_name) {
    var element_id = (element_name) ? ('#' + element_name + "-input") : "#email-input";
    var val = $(element_name).val();
    val = $.trim(val);
    if (val.length && val.indexOf('@') < 0) {
        errors.push("EMail должен содержать знак '@'");
    }
}

function xsm_ank_check_control_question(errors, mode) {
    var val = $("#control_question-input").val();
    val = $.trim(val);
    if (mode == "fizlesh") {
        if (!(
            val.indexOf("ампер") >= 0 ||
            val.indexOf("Ампер") >= 0 ||
            val == "А" ||  // rus
            val == "а" ||  // rus
            val == "A" ||  // eng
            val == "a"  // eng
        )) {
            errors.push("Неправильный ответ на контрольный вопрос. Вспомните физику!");
        }
    } else if (mode == "med_olymp") {
        if (!(
            val.indexOf("пять") >= 0 ||
            val.indexOf("Пять") >= 0 ||
            val == "5"
        )) {
            errors.push("Неправильный ответ на контрольный вопрос. Посмотрите на свою руку!");
        }
    }
}

function xsm_ank_check_phone(id, nDigit) {
    var val = $(id).val();
    val = $.trim(val);
    var valLenTest = val.replace(/[^0-9]/g, '');
    if (valLenTest.length < nDigit)
        return "телефон должен содержать не меньше " + nDigit + " цифр. ";
    return '';
}

function xsm_ank_check_phones(aError) {
    var sPhError = xsm_ank_check_phone("#phone-input", 7);
    var sCellError = xsm_ank_check_phone("#cellular-input", 9);
    if (sPhError.length && sCellError.length)
        aError.push("Укажите правильно хотя бы один из телефонов! Домашний " +
            sPhError + "Мобильный " + sCellError);
}

function xsm_ank_check_empty(id, sDesc, aResult) {
    var val = $(id).val();
    val = $.trim(val);
    if (val.length < 2) {
        aResult.push("Вы не указали " + sDesc);
    }
}

function WarnPersonal(aWarning) {
    xsm_ank_check_empty("#favourites-text", "любимые предметы", aWarning);
    xsm_ank_check_empty("#achievements-text", "достижения", aWarning);
    xsm_ank_check_empty("#hobby-text", "хобби", aWarning);
    //xsm_ank_check_empty("#lesh_ref-text", "откуда Вы узнали о школе", aWarning);
}

function xsm_ank_make_list(aList) {
    var sRes = '<ul class="ankMessageList">';
    for (var i = 0; i < aList.length; ++i)
        sRes += ("<li>" + aList[i] + "</li>");
    return sRes + "</ul>";
}

var GShowWarning = true;

function xsm_ank_setup_fizlesh() {
    $("#favourites-text").change(xsm_ank_on_change);
    $("#achievements-text").change(xsm_ank_on_change);
    $("#hobby-text").change(xsm_ank_on_change);

    $("#submit_anketa-submit").click(function() {
        var aError = [];
        xsm_ank_check_name(aError, "last_name", "Фамилия");
        xsm_ank_check_name(aError, "first_name", "Имя");
        xsm_ank_check_name(aError, "patronymic", "Отчество");
        xsm_ank_check_birth_date(aError, "birth_date", "Дата рождения");
        xsm_ank_check_class(aError);
        xsm_ank_check_phones(aError);
        xsm_ank_check_email(aError);
        xsm_ank_check_control_question(aError, "fizlesh");

        var aWarning = [];
        WarnPersonal(aWarning);

        var bResult = true;
        if (aError.length) {
            $("#t-Error").html(xsm_ank_make_list(aError));
            bResult = false;
        } else {
            $("#t-Error").html(' ');
        }

        if (aWarning.length) {
            var sWarning = xsm_ank_make_list(aWarning);
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
}

function xsm_ank_collect_phone_errors(errors, element_id) {
    var phone_error = xsm_ank_check_phone(element_id, 9);
    if (phone_error.length) {
        errors.push(phone_error);
    }
}

function xsm_ank_setup_med_olymp() {
    $('#submit_anketa-submit').click(function() {
        var errors = [];
        xsm_ank_check_name(errors, "last_name", "Фамилия");
        xsm_ank_check_name(errors, "first_name", "Имя");
        xsm_ank_check_name(errors, "patronymic", "Отчество");
        xsm_ank_check_birth_date(errors, "birth_date", "Дата рождения");
        xsm_ank_check_class(errors);
        xsm_ank_collect_phone_errors(errors, "cellular");
        xsm_ank_collect_phone_errors(errors, "parent_phone");
        xsm_ank_check_phones(errors);
        xsm_ank_check_name(errors, "parent_fio", "ФИО родителя");
        xsm_ank_check_email(errors, "email");
        xsm_ank_check_email(errors, "parent_email");
        xsm_ank_check_control_question(errors, "med_olymp");

        var check_result = true;
        if (errors.length) {
            $("#t-Error").html(xsm_ank_make_list(errors));
            check_result = false;
        } else {
            $("#t-Error").html(' ');
        }

        if (!errors.length) {
            $("#c-Message").hide();
        } else {
            $("#c-Message").show();
        }
        return check_result;
    });
}


$(document).ready(function() {
    if ($('#favourites-text')) {
        // FizLesh anketa, default
        xsm_ank_setup_fizlesh();
        console.log("qqq");
    } else if ($('#department_id-input').val() == "8") {
        xsm_ank_setup_med_olymp();
        console.log("zzz");
    }
});
