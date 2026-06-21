from django.contrib import admin
from django.utils.html import format_html
from apps.blogs.models import BlogCategory, BlogTag, BlogPost

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'published_at', 'image_preview')
    list_filter = ('status', 'category', 'published_at')
    search_fields = ('title', 'content', 'meta_title', 'meta_description')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    fieldsets = (
        ('Blog Content', {
            'fields': ('title', 'slug', 'category', 'tags', 'featured_image', 'content')
        }),
        ('Status & Scheduling', {
            'fields': ('status', 'published_at')
        }),
        ('SEO Meta Data (Google optimization)', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" height="40" style="object-fit:contain;" />', obj.featured_image.url)
        return "-"
    image_preview.short_description = "Featured Image"
