"""
WSGI config for YaMDb project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

<<<<<<< HEAD
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api_yamdb.settings")
=======
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_yamdb.settings')
>>>>>>> 1e3f07e9477cd5eea8569af60f91ffb48f5ea796

application = get_wsgi_application()
