import os

from django import template
from django.conf import settings

register = template.Library()
NOTICE_JS = getattr(settings, 'NOTICE_JS', None)

@register.inclusion_tag('display_notice.html')
def display_notice():
    return {}

@register.simple_tag
def include_notice():
    global NOTICE_JS
    if not NOTICE_JS:
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        NOTICE_JS = open(os.path.join(path, 'media', 'js', 'jquery.notice.js')).read()
    return '''<script type="text/javascript">%s</script>''' % NOTICE_JS
