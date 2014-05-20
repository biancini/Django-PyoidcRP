import os
import sys

path = "/var/www/"
if path not in sys.path:
    sys.path.append(path)

path = "/var/www/django_rp"
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_rp.settings")

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
