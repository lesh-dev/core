/**
 * Hook providing auto-submit on form controls change
 **/
function xsm_filter_form_autosubmit()
{
    $(document).ready(function() {
        var form_selector = "#filter-form";
        var form = $(form_selector);
        _set_submit_on_control_type(form, form_selector, "input");
        _set_submit_on_control_type(form, form_selector, "select");
    });
}

function _set_submit_on_control_type(form, form_selector, element_type)
{
    var controls = form.find(element_type);
    for (var i = 0; i < controls.length; ++i)
    {
        var control = controls[i];
        $(control).change(function() {
            $(form_selector).submit();
        });
    }
}

function _find_row(ele)
{
    while (ele && ele.prop('nodeName') != 'TR') {
        ele = ele.parent();
    }
    return ele;
}

function _default_handler(response)
{
    if (!response)
    {
        console.log("Got empty Ajax response");
        alert("Got empty Ajax response");
        return false;
    }
    if (!response["status"])
    {
        alert("No response status in Ajax response");
        console.log("Ajax response: " + response);
        return false;
    }
    if (response["status"] != "ok")  // XSM_API_STATUS_OK
    {
        alert("Ajax response status is not OK");
        console.log("Ajax response status: " + response["status"]);
        return false;
    }
    return true;
}

function _update_data(cell, new_content)
{
    var field_name = cell.attr('field-name');
    var data = {};
    data[field_name] = new_content;

    var id = _find_row(cell).attr('row-id');
    var json_data = JSON.stringify(data);
    var encoded_data = encodeURIComponent(json_data);
    xsm_async_call('/xsm/api/update/person/' + id + '/' + encoded_data);
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
    xsm_async_call(enum_value_url, function (response) {
        cell.html(response['enum_value']);
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

/**
 * Generic Ajax caller for JSON XSM API
 * @param url query url
 * @param on_success callback function that will be called on success request.
 * Contains generic error handler.
 **/
function xsm_async_call(url, on_success)
{
    var on_failure = function(response) {
        console.log('Failed ajax response: ' + response);
        alert('Ajax request failed, please mail to dev@fizlesh.ru (see JS console for bogus server response).');
    };
    jQuery.get({
        url: url,
        success: function(response) {
            if (!_default_handler(response))
                return;

            if (on_success)
                on_success(response);
        },
        failure: on_failure
    });
}

/**
 * Grid cell edit handler
 */
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

    jQuery.get('/xsm/api/get/person/' + id, function(response) {
        var original_value = response["object"][field_name];
        cell.addClass("cell-editing");

        if (enum_type)
        {
            // enum
            if (!String(original_value).length) {
                original_value = 'some_undefined_value';
            }

            var enum_url = '/xsm/api/enum_html/' + field_name + '/' + original_value + '/' + enum_type;
            xsm_async_call(enum_url, function(response) {
                // turn cell into input
                cell.html(response['enum_html']);
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


g_xsm_sort_state = new Array();

/**
 * Provide multicolumn sort handling via
 * click or shift+click on column header.
 */
function xsm_column_header_click_handler(event)
{
    var element = event.currentTarget;
    var id = element.id;

    var sort_name = id.replace("sort_by_", "");
    if (event.shiftKey)
    {
        var found = false;
        // prevent duplicates in sort vector
        for (var i = 0; i < g_xsm_sort_state.length; ++i)
        {
            if (g_xsm_sort_state[i] == sort_name)
            {
                g_xsm_sort_state[i] = "-" + sort_name;
                found = true;
                break;
            }
            else if (g_xsm_sort_state[i] == "-" + sort_name)
            {
                g_xsm_sort_state[i] = sort_name;
                found = true;
            }
        }
        if (!found)
        {
            g_xsm_sort_state.push(sort_name);
        }
    }
    else
    {
        if (g_xsm_sort_state.length == 1 && g_xsm_sort_state[0] == sort_name)
        {
            // not empty state and one column with positive sort
            g_xsm_sort_state = ["-" + sort_name];
        }
        else
        {
            // negative sorting or any other
            g_xsm_sort_state = [sort_name];
        }
    }
    var show_sort_column = g_xsm_sort_state.join(",");
    window.location = "/xsm/list-person-locator&show_sort_column=" + show_sort_column;
}

$(function() {
    $("span.sort_by_inner").click(xsm_column_header_click_handler);
});
