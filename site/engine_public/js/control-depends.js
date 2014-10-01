function xjs_is_too_small_text(id)
{
    var ele = $('#' + id);
    var min_length = ele.data('dep-min-length');
    if (!min_length)
        min_length = 10;
    var val = ele.val();
    val = $.trim(val);
    return (val.length < min_length);
}

function xjs_check_custom_dep_handler(id)
{
    var control = $('#' + id);
    var handler = control.data('custom-dep-handler');
    if (!handler)
        return null;
    return handler(id);
}

function xjs_toggle_element(id, enabled, reason)
{
    if (!reason)
        reason = ''

    var node = $('#' + id);
    if (enabled)
    {
        node.removeAttr('disabled')
        node.removeClass('input-disabled');
        node.removeAttr('title')
    }
    else
    {
        node.attr('disabled', 'disabled');
        node.addClass('input-disabled');
        node.attr('title', reason)
    }
}

function xjs_check_dependencies(id)
{
    var deps = $('#' + id).data('dependencies');
    if (!deps)
    {
        alert('Checking node with no dependencies. ');
        return;
    }

    var reason = "";

    var enabled = true;
    for (var i = 0; i < deps.length; ++i)
    {
        var dep_id = deps[i];
        var custom_result = xjs_check_custom_dep_handler(dep_id)
        if (custom_result !== null)
        {
            enabled = enabled && custom_result['valid'];
            reason += custom_result['reason'];
            continue;
        }
        if (xjs_is_too_small_text(dep_id))
        {
            reason += "Слишком мало текста в поле '" + $('#' + dep_id).attr('placeholder') + "'. ";
            enabled = false;
        }
    }
    xjs_toggle_element(id, enabled, reason);
}

/**
  * This should be used to set dependencies
  **/
function xjs_set_depends_on(id, dependency_id, custom_handler, min_length)
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
    if (min_length)
        dep_node.data('dep-min-length', min_length);

    dep_node.change(xjs_check_dependencies.bind(null, id));
    dep_node.bind('input', xjs_check_dependencies.bind(null, id));

    // check dependencies for the first time (initial state)
    xjs_check_dependencies(id);
}

/**
  * Deferred variant of `xjs_set_depends_on`
  **/
function xjready_set_depends_on(id, dependency_id, custom_handler, min_length)
{
    $(document).ready(function() {
        xjs_set_depends_on(id, dependency_id, custom_handler, min_length);
    });
}