import os
import sys
import site

import django.core.handlers.wsgi
from django.conf import settings

# Set the django settings env
os.environ['DJANGO_SETTINGS_MODULE'] = 'noticeapp.settings'

# Set env variables.
PROJECT_PATH = getattr(settings, 'PROJECT_PATH')
print PROJECT_PATH
sys.path.append(PROJECT_PATH)
site.addsitedir(os.path.join(PROJECT_PATH, '/ve/lib/python2.6/site-packages'))

# define the wsgi app
application = django.core.handlers.wsgi.WSGIHandler()

# Mount the application to the url
applications = {'':'application', }
