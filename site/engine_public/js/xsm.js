/**
 * Hook providing auto-submit on form controls change
 */
function xsm_filter_form_autosubmit()
{
    $(document).ready(function() {

        var form = $('#filter-form');
        var controls = form.find('input');
        for (var i in controls)
        {
            var control = controls[i];
            $(control).change(function() {
                $('#filter-form').submit();
            });
        }
    });
}


function _find_row(ele)
{
    while (ele && ele.prop('nodeName') != 'TR') {
        ele = ele.parent();
    }
    return ele;
}

function _update_data(cell, new_content)
{
    var field_name = cell.attr('field-name');
    var data = {};
    data[field_name] = new_content;

    var id = _find_row(cell).attr('row-id');
    var json_data = JSON.stringify(data);
    var encoded_data = encodeURIComponent(json_data);
    jQuery.get('/xsm/api/update/person/' + id + '/' + encoded_data, function(data) {
        // console.log(data["status"]);
    });
}


function _xsm_edit_field_keypress_handler(event)
{
    if (event.which == 13)
    {
        var new_content = $(this).val();
        var cell = $(this).parent();
        cell.text(new_content);
        cell.removeClass("cell-editing");
        _update_data(cell, new_content);
        event.stopPropagation();
        return false;
    }
}

function _enum_value_handler(cell, value, enum_type)
{
    var field_name = cell.attr('field-name');
    var enum_value_url = '/xsm/api/enum_value_html/' + field_name + '/' + value + '/' + enum_type;
    xsm_async_call(enum_value_url, function (result) {
        cell.html(result['enum_value']);
        cell.removeClass("cell-editing");
    });
}

function _text_value_handler(cell, value)
{
    cell.text(value);
    cell.removeClass("cell-editing");
}

function _xsm_edit_field_enum_change(event)
{
    var new_content = $(this).val();
    var cell = $(this).parent();
    var enum_type = cell.attr('enum-type');
    if (enum_type)
        _enum_value_handler(cell, new_content, enum_type);
    else
        _text_value_handler(cell, new_content);
    _update_data(cell, new_content);
    event.stopPropagation();
    return false;
}

function xsm_async_call(url, on_success)
{
    var on_failure = function(response) {
        console.log('Failed ajax response: ' + response);
        alert('Ajax request failed, please mail to dev@fizlesh.ru (see JS console for bogus server response).');
    };
    jQuery.get({
        url: url,
        success: on_success,
        failure: on_failure
    });
}


function xsm_edit_field_handler(event)
{
    var cell = $(this);
    var field_name = cell.attr('field-name');
    if (!field_name) {
        // disable handlers for this cell
        return;
    }

    var enum_type = cell.attr('enum-type');
    var id = _find_row(cell).attr('row-id');

    jQuery.get('/xsm/api/get/person/' + id, function(data) {
        var original_value = data["object"][field_name];
        cell.addClass("cell-editing");

        if (enum_type)
        {
            // enum
            var enum_url = '/xsm/api/enum_html/' + field_name + '/' + original_value + '/' + enum_type;
            xsm_async_call(enum_url, function(result) {
                // turn cell into input
                cell.html(result['enum_html']);
                var input = cell.children().first();
                input.focus();
                input.change(_xsm_edit_field_enum_change);

                var cancel_handler = function() {
                    _enum_value_handler(cell, original_value, enum_type);
                };
                input.blur(cancel_handler);
            });

        }
        else
        {
            // text control
            cell.html('<input type="text" />');
            var input = cell.children().first();
            input.focus();
            input.keypress(_xsm_edit_field_keypress_handler);
            input.val(original_value);
            var cancel_handler = function() {
                _text_value_handler(cell, original_value);
            };
            input.blur(cancel_handler);
        }
    });

    // finish event
    event.stopPropagation();
    return false;
}

/**
 * Install editor on each cell
 **/
function xsm_set_editors()
{
    $("td").dblclick(xsm_edit_field_handler);
}
