import six
import json
import logging
import cornice.pyramidhook as hooks
from pyramid import httpexceptions
from boltons import tbutils

log = logging.getLogger(name="mediapublic.{}".format(__name__))


def handle_exceptions(exc, request):
    # At this stage, the checks done by the validators had been removed because
    # a new response started (the exception), so we need to do that again.
    if not isinstance(exc, httpexceptions.HTTPException):
        e = tbutils.ExceptionInfo.from_current()

        exc_info = {
            'error': e.exc_msg,
            'exception': e.to_dict(),
            'traceback': e.tb_info.get_formatted(),
        }
        exc_info['exception'].pop('exc_tb')
        request.response.status = 500
        request.response.body = six.b(json.dumps(exc_info, indent=2))
        return request.response
    request.info['cors_checked'] = False
    return hooks.apply_filters(request, exc)
