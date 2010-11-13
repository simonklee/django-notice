import os
from django import template
import messages

register = template.Library()

MESSAGES_JS = None
def include_messages():
    global MESSAGES_JS
    if MESSAGES_JS is None:
        MESSAGES_JS = open(os.path.join(os.path.dirname(messages.__file__), 'media', 'js', 'jqueryMessages.js')).read()
    return '''<script type="text/javascript">%s</script>''' % MESSAGES_JS
register.simple_tag(include_messages)
