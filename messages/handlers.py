import datetime
import calendar

from django.http import HttpResponse
from piston.handler import BaseHandler

from messages import get_messages()


class MessagesHandler(BaseHandler):
    allowed_methods = ('GET',)

    def read(self, request):
        if request.user.is_anonymous():
            return rc.FORBIDDEN
        return get_messages(request.user)
