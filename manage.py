#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
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
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
