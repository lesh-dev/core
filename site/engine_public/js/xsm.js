function xsm_filter_form_autosubmit()
{
    var form = $('#filter-form');
    var controls = form.find('input');
    for (var i in controls)
    {
        var control = controls[i];
        $(control).change(function() {
            $('#filter-form').submit();
        });
    }
}

function xsm_is_too_small_text(id)
{
    var val = $('#' + id).val();
    val = $.trim(val);
    return (val.length < 10);
}

function xsm_check_custom_dep_handler(id)
{
    var control = $('#' + id);
    var handler = control.data('custom-dep-handler');
    if (!handler)
        return null;
    return handler(id);
}

function xsm_toggle_element(id, enabled)
{
    var node = $('#' + id);
    if (enabled)
    {
        node.removeAttr('disabled')
        node.removeClass('input-disabled');
    }
    else
    {
        node.attr('disabled', 'disabled');
        node.addClass('input-disabled');
    }
}

function xsm_check_dependencies(id)
{
    var deps = $('#' + id).data('dependencies');
    if (!deps)
    {
        alert('Checking node with no dependencies. ');
        return;
    }

    var enabled = true;
    for (var i in deps)
    {
        var custom_result = xsm_check_custom_dep_handler(deps[i])
        if (custom_result !== null)
        {
            enabled = enabled && custom_result;
            continue;
        }

        if (xsm_is_too_small_text(deps[i]))
            enabled = false;
    }
    xsm_toggle_element(id, enabled);
}

function xsm_set_depends_on(id, dependency_id, custom_handler)
{
    var node = $('#' + id);
    var deps = node.data('dependencies');
    if (!deps)
        deps = [];

    deps.push(dependency_id);
    node.data('dependencies', deps);
    var dep_node = $('#' + dependency_id);
    if (custom_handler)
        dep_node.data('custom-dep-handler', custom_handler);

    dep_node.change(xsm_check_dependencies.bind(null, id));
    dep_node.bind('input', xsm_check_dependencies.bind(null, id));

    // check dependencies for the first time (initial state)
    xsm_check_dependencies(id);
}
