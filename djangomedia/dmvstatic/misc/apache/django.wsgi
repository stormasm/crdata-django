import os, sys
sys.path.append('/mnt/store/django')
os.environ['DJANGO_SETTINGS_MODULE'] = 'dmv.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
