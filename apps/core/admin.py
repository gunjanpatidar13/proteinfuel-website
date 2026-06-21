from django.contrib import admin
from django.utils.html import format_html
from apps.core.models import (
    SiteSettings, HomepageContent, WhyChooseItem, Testimonial,
    GalleryItem, FAQ, ContactInquiry, FranchiseApplication,
    Job, JobApplication, StatCard, SocialLink, NewsletterSubscriber
)

class SingletonAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Allow addition only if no records exist yet
        return self.model.objects.count() == 0

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonAdmin):
    list_display = ('site_name', 'contact_email', 'contact_phone', 'updated_at')
    fieldsets = (
        ('General Info', {
            'fields': ('site_name', 'logo', 'logo_dark')
        }),
        ('Contact Details', {
            'fields': ('contact_email', 'contact_phone', 'contact_address')
        }),
        ('Footer & Credits', {
            'fields': ('footer_about', 'copyright_text')
        }),
        ('SEO & Analytics', {
            'fields': ('google_analytics_id', 'meta_title', 'meta_description')
        }),
        ('Meta Files Override', {
            'fields': ('robots_txt', 'sitemap_xml'),
            'classes': ('collapse',)
        }),
    )


@admin.register(HomepageContent)
class HomepageContentAdmin(SingletonAdmin):
    list_display = ('hero_headline', 'updated_at')
    fieldsets = (
        ('Hero Section', {
            'fields': ('hero_headline', 'hero_subheadline', 'hero_button_text', 'hero_button_url', 'hero_image')
        }),
        ('Why Choose Us Section Header', {
            'fields': ('why_choose_title', 'why_choose_subtitle')
        }),
        ('Nutrition Philosophy Header', {
            'fields': ('nutrition_title', 'nutrition_content')
        }),
        ('CTA Section', {
            'fields': ('cta_title', 'cta_subtitle', 'cta_button_text', 'cta_button_url')
        }),
    )


@admin.register(WhyChooseItem)
class WhyChooseItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon_name', 'is_active', 'display_order')
    list_editable = ('is_active', 'display_order')
    search_fields = ('title', 'description')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'rating', 'is_active', 'display_order', 'image_preview')
    list_editable = ('is_active', 'display_order')
    search_fields = ('customer_name', 'review_text')
    list_filter = ('rating', 'is_active')

    def image_preview(self, obj):
        if obj.customer_image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius:50%; object-fit:cover;" />', obj.customer_image.url)
        return "-"
    image_preview.short_description = "Preview"


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'display_order', 'image_preview')
    list_editable = ('is_active', 'display_order')
    search_fields = ('title',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" style="max-height:50px; object-fit:contain;" />', obj.image.url)
        return "-"
    image_preview.short_description = "Image"


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'is_active', 'display_order')
    list_editable = ('is_active', 'display_order')
    search_fields = ('question', 'answer')


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'is_resolved', 'created_at')
    list_filter = ('is_resolved', 'created_at')
    search_fields = ('name', 'email', 'phone', 'message')
    readonly_fields = ('name', 'email', 'phone', 'message', 'created_at')


@admin.register(FranchiseApplication)
class FranchiseApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'investment_budget', 'is_reviewed', 'created_at')
    list_filter = ('is_reviewed', 'created_at')
    search_fields = ('name', 'email', 'phone', 'city', 'message')
    readonly_fields = ('name', 'phone', 'email', 'city', 'investment_budget', 'message', 'created_at')


class JobApplicationInline(admin.TabularInline):
    model = JobApplication
    extra = 0
    readonly_fields = ('name', 'email', 'phone', 'resume', 'cover_letter', 'created_at')
    can_delete = False


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('position', 'location', 'status', 'created_at')
    list_filter = ('status', 'location', 'created_at')
    search_fields = ('position', 'location', 'description')
    inlines = [JobApplicationInline]


@admin.register(StatCard)
class StatCardAdmin(admin.ModelAdmin):
    list_display = ('value', 'label', 'is_active', 'display_order')
    list_editable = ('is_active', 'display_order')
    search_fields = ('label',)


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('platform_name', 'url', 'icon_name', 'is_active', 'display_order')
    list_editable = ('is_active', 'display_order')
    search_fields = ('platform_name',)


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('email',)
