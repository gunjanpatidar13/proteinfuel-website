from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # CKEditor uploader routes
    path('ckeditor/', include('ckeditor_uploader.urls')),
    
    # Custom Apps Routes
    path('products/', include('apps.catalog.urls', namespace='catalog')),
    path('blog/', include('apps.blogs.urls', namespace='blogs')),
    path('', include('apps.core.urls', namespace='core')),
]

# Serve media and static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Global custom error handlers
handler404 = 'apps.core.views.error_404_view'
handler500 = 'apps.core.views.error_500_view'

# Catch-all pattern to render custom 404 template for undefined URLs in development mode (DEBUG = True)
from django.urls import re_path
from apps.core.views import error_404_view

urlpatterns += [
    re_path(r'^.*/$', error_404_view),
]
