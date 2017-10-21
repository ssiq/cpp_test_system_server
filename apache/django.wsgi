import os
import sys

path = '/home/zt/tmp'
if path not in sys.path:
    sys.path.insert(0, path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'cpp_test_system_server.settings'
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()