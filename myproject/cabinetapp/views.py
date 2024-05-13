def _cabinet_id(request):
    """
    Get the cabinet by session_key present in the session
    :param request:
    :return: cabinet by particular session key
    """
    cabinet = request.session.session_key
    if not cabinet:
        cabinet = request.session.create()
    return cabinet


def cabinet_index(request):
    return
