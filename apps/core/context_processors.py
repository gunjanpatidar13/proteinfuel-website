from apps.core.models import SiteSettings, SocialLink
from apps.catalog.models import Category

def global_site_settings(request):
    """
    Injects site-wide settings and social links into every template context.
    """
    # Load site settings singleton
    settings = SiteSettings.load()
    
    # Retrieve active social links
    social_links = SocialLink.objects.filter(is_active=True)
    
    # Retrieve active product categories for header/footer menu
    header_categories = Category.objects.filter(is_active=True)[:6]

    return {
        'site_settings': settings,
        'social_links': social_links,
        'header_categories': header_categories,
    }
