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
