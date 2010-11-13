from django.http import HttpResponse
from piston.handler import BaseHandler

from backend import get_messages


class MessageHandler(BaseHandler):
    allowed_methods = ('GET',)

    def read(self, request):
        if request.user.is_anonymous():
            return rc.FORBIDDEN
        return dict(zip(('valid', 'messages'), get_messages(request.user)))
