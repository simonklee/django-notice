from django.conf.urls.defaults import *
from piston.resource import Resource

from messages.handlers import MessagesHandler

messages = Resource(handler=MonHandler)

urlpatterns = patterns('',
    url(r'^get_messages$', messages, name = 'messages_get_messages'),
)
