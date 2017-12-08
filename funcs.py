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