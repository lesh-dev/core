function FilterFormAutoSubmit()
{
    var form = $('#filter-form');
    var controls = $(form).find('input');
    for (var i in controls)
    {
        var control = controls[i];
        $(control).change(function() {
            var form = $('#filter-form');
            form.submit();
        });
    }
}


function xsm_is_too_small_text(id)
{
    var val = $(id).val();
    val = $.trim(val);
    return (val.length < 2);
}


function xsm_check_dependencies(id)
{
    var deps = $(id).data('dependencies');
    if (!deps)
    {
        alert('Checking node with no dependencies. ');
        return;
    }

    var enable = true;
    for (var i in deps)
    {
        dependency_id = deps[i];
        if (xsm_is_too_small_text(deps[i]))
            enable = false;
    }
    console.log(enable);

    if (enable)
        $(id).removeAttr('disabled')
    else
        $(id).attr('disabled', 'disabled');
}


function xsm_set_depends_on(id, dependency_id)
{
    var node = $(id);
    var deps = node.data('dependencies');
    if (!deps)
        deps = [];

    deps.push(dependency_id);
    $(id).data('dependencies', deps);
    $(dependency_id).change(xsm_check_dependencies.bind(null, id));
}