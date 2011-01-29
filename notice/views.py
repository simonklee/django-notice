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
from django.contrib.auth.decorators import login_required, user_passes_test
from simplejson import JSONEncoder

from backend import get_notices, push_notice

class LazyEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_unicode(obj)
        return obj

@user_passes_test(lambda u: u.is_superuser)
def add(request):
    if request.method != 'POST':
        return HttpResponse(content="", status=401)

    notice = request.POST['notice']

    try:
        pk = request.POST['user']
        user = User.objects.get(pk)
    except KeyError:
        user = request.user

    push_notice(user, notice)
    return HttpResponse(
        JSONEncoder().encode({'valid': True}),
        mimetype='application/json')

@login_required
@condition(etag_func=None)
def get(request):
    data = notice_listener(request.user, {})
    resp = HttpResponse(data, mimetype='application/json')
    resp['Transfer-Encoding'] = 'chunked'
    return resp

def notice_listener(user, context, interval=1):
    while True:
        notices = get_notices(user)
        if notices:
            yield JSONEncoder().encode({'notices': notices})
            raise StopIteration()

        yield ''
        uwsgi.green_pause(1)
