from django.http import Http404


def clean_data(data, data_type):
    """
    making sure that data has specified format or can be converted to it
    """
    try:
        data = data_type(data)
    except ValueError:
        raise Http404('unexpected data %s passed, could not convert to a suitable format %s' % (data, data_type))
    else:
        return data


def signal(msg):
    pass


def turn_integer(val):
    try:
        val = int(val)
    except ValueError:
        raise Http404('failed to convert "%s" into integer' % val)
    return val


def check_positive(val):
    if not val > 0:
        raise Http404('value "%s" is not positive' % val)
    else:
        return val
