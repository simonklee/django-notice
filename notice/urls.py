from django.conf.urls.defaults import *
from piston.resource import Resource

from handlers import MessageHandler

mes = Resource(handler=MessageHandler)

urlpatterns = patterns('',
    url(r'^get_notices$', mes, name = 'notice_get_notices'),
)
