"""Module containing generic utilies for Craton."""


def copy_project_id_into_json(context, json, project_id_key='project_id'):
    """Copy the project_id from the context into the JSON request body.

    :param context:
        The request context object.
    :param json:
        The parsed JSON request body.
    :returns:
        The JSON with the project-id from the headers added as the
        "project_id" value in the JSON.
    :rtype:
        dict
    """
    json[project_id_key] = getattr(context, 'tenant', '')
    return json
