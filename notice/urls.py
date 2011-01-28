from django.conf.urls.defaults import *

urlpatterns = patterns('notice.views',
    url(r'^get_notices/$', 'notices', name='notice_get_notices'),
)
