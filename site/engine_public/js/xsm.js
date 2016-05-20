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


function _xsm_edit_field_keypress_handler(event)
{
    if (event.which == 13)
    {
        var new_content = $(this).val();
        var cell = $(this).parent();
        cell.text(new_content);
        cell.removeClass("cell-editing");
        field_name = cell.attr('field-name')
        data = {}
        data[field_name] = new_content;
        var ele = cell;
        while (ele && ele.prop('nodeName') != 'TR') {
            ele = ele.parent();
        }

        id = ele.attr('row-id');
        json_data = JSON.stringify(data);
        encoded_data = encodeURIComponent(json_data);
        jQuery.get('/xsm/api/update/person/' + id + '/' + encoded_data, function(data) {
            // console.log(data["status"]);
        });

        event.stopPropagation();
        return false;
    }
}


function xsm_edit_field_handler(event)
{
    var original_content = $(this).text();
    $(this).addClass("cell-editing");
    $(this).html('<input type="text"/>');
    var input = $(this).children().first();
    input.focus();
    input.keypress(_xsm_edit_field_keypress_handler);
    input.val(original_content);

    // closure is here to original content (it's better to save it via data())
    input.blur(function() {
        var cell = $(this).parent();
        cell.text(original_content);
        cell.removeClass("cell-editing");
    });
    event.stopPropagation();
    return false;
}


function xsm_set_editors()
{
    $("td").dblclick(xsm_edit_field_handler);
}
