"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Monkeypatch force_text for django-ckeditor compatibility with Django 4.2+
import django.utils.encoding
django.utils.encoding.force_text = django.utils.encoding.force_str

# Monkeypatch django.conf.urls.url to django.urls.re_path for django-ckeditor compatibility
import django.conf.urls
from django.urls import re_path
django.conf.urls.url = re_path

# Monkeypatch render_to_response for django-ckeditor compatibility
import django.shortcuts
def render_to_response(template_name, context=None, content_type=None, status=None, using=None):
    return django.shortcuts.render(None, template_name, context, content_type, status, using)
django.shortcuts.render_to_response = render_to_response

application = get_wsgi_application()
