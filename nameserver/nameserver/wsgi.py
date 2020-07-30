"""
WSGI config for nameserver project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application


# 2020-07-15 KWS Added by KWS
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'nameserver.settings'


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nameserver.settings')

application = get_wsgi_application()
