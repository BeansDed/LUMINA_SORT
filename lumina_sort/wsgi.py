"""
WSGI config for lumina_sort project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lumina_sort.settings')

application = get_wsgi_application()
