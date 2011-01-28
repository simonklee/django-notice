from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'noticeapp.foo.views.index',
        {'template_name': 'foo/index.html'},
        name='index'),
)
