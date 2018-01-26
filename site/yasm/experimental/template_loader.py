import jinja2


def no_request_render_template(path, template_name, **context):
    """
    Renders templates not using default flask app
    :param path: path to templates directory
    :param template_name: string
    :param context: dictionary
    :return: rendered template
    """
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(path)  # TODO: make template loader appropriate
    )                                                                    # Should we make our little template manager?
    template = env.get_template(template_name)
    return template.render(**context)
