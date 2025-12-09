"""
ASGI config for lumina_sort project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lumina_sort.settings')

application = get_asgi_application()
