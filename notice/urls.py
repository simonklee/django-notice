from django.conf.urls.defaults import *

urlpatterns = patterns('notice.views',
    url(r'^get/$', 'get', name='notice_get'),
    url(r'^add/$', 'add', name='notice_add'),
)
