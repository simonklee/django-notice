import sys
import time

try:
    import uwsgi
except ImportError:
    pass
   # raise ImportError('uWSGI is required to run this package')

from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response as render
from django.template import RequestContext
from django.utils.functional import Promise
from django.views.decorators.http import condition
from simplejson import JSONEncoder

from backend import get_notices

class LazyEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_unicode(obj)
        return obj

@condition(etag_func=None)
def notices(request):
    if request.user.is_anonymous():
        return HttpResponse(content="", status=401)
    user = request.user

    data = pull_notices(user, {})
    resp = HttpResponse(data, mimetype='application/json')
    resp['Transfer-Encoding'] = 'chunked'
    return resp

def pull_notices(user, context, interval=1):
    print 'started'
    yield ''
    i = 0
    while True:
        print '.'
        notices = get_notices(user)
        if notices[0]:
            yield JSONEncoder().encode(dict(zip(('valid', 'notices'), notices)))
            break
        yield ''

        if i > 1:
            uwsgi.green_pause(1)
        else:
            i = i + 1
