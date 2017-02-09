def format_variables(args, obj):
    """Update resource response with requested type of variables."""
    resolved_values = args["resolved-values"]
    if resolved_values:
        obj.vars = obj.resolved
    else:
        obj.vars = obj.variables
    return obj
