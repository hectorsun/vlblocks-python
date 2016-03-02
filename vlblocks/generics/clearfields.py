def clearfields(d, *fields):
    if not isinstance(d, dict):
        raise TypeError
    for f in fields:
        if d.has_key(f):
            del d[f]

    return d
