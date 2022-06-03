"""
ASGI config for YaMDb project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

<<<<<<< HEAD
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api_yamdb.settings")
=======
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_yamdb.settings')
>>>>>>> 1e3f07e9477cd5eea8569af60f91ffb48f5ea796

application = get_asgi_application()
