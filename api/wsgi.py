"""
WSGI config for api project.

It exposes the WSGI callable as a module-level variable named ``app``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')

app = get_wsgi_application()


# import os
# from django.conf import settings
# from django.core.wsgi import get_wsgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')

# application = get_wsgi_application()

# # THIS IS THE ONLY LINE THAT FIXES CSS + PREVENTS CRASH ON VERCEL
# if not settings.DEBUG:
#     from django.contrib.staticfiles.views import serve
#     from django.urls import re_path
#     from django.contrib.staticfiles.handlers import StaticFilesHandler
    
#     application = StaticFilesHandler(application)
