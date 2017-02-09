def format_variables(args, obj):
    """Update resource response with requested type of variables."""
    if args:
        resolved_values = args["resolved-values"]
    else:
        resolved_values = None

    if resolved_values:
        obj.vars = obj.resolved
    else:
        obj.vars = obj.variables
    return obj
