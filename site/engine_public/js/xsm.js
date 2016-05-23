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

        var id = _find_row(cell).attr('row-id');
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
    var cell = $(this);
    field_name = cell.attr('field-name')
    var enum_type = cell.attr('enum-type')
    var id = _find_row(cell).attr('row-id');

    jQuery.get('/xsm/api/get/person/' + id, function(data) {
        var original_content = data["object"][field_name];
        cell.addClass("cell-editing");

        if (enum_type)
        {
            // enum
            jQuery.get('/xsm/api/enum_html/' + field_name + '/' + original_content + '/' + enum_type, function(enum_data) {
                cell.html(enum_data.enum);
                var input = cell.children().first();
                input.focus();

                // closure is here to original content (it's better to save it via data())
                input.blur(function() {
                    cell.text(original_content);
                    cell.removeClass("cell-editing");
                });

            });

        }
        else
        {
            // text control
            cell.html('<input type="text"/>');
            var input = cell.children().first();
            input.focus();
            input.keypress(_xsm_edit_field_keypress_handler);
            input.val(original_content);

            // closure is here to original content (it's better to save it via data())
            input.blur(function() {
                cell.text(original_content);
                cell.removeClass("cell-editing");
            });
        }
    });

    // finish event
    event.stopPropagation();
    return false;
}


function xsm_set_editors()
{
    $("td").dblclick(xsm_edit_field_handler);
}
