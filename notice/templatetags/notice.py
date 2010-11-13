import os
from django import template

import notice

register = template.Library()

NOTICE_JS = None
def include_notice():
    global NOTICE_JS
    if NOTICE_JS is None:
        path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
        NOTICE_JS = open(os.path.join(path, 'media', 'js', 'jquery.notice.js')).read()
    return '''<script type="text/javascript">%s</script>''' % NOTICE_JS
register.simple_tag(include_notice)
