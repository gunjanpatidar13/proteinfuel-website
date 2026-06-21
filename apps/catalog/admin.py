from django.contrib import admin
from django.utils.html import format_html
from apps.catalog.models import Category, Product, ProductImage, NutritionalProfile

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 2
    fields = ('image', 'is_primary', 'display_order', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="50" style="object-fit:contain;" />', obj.image.url)
        return "-"
    image_preview.short_description = "Preview"


class NutritionalProfileInline(admin.StackedInline):
    model = NutritionalProfile
    can_delete = False
    fieldsets = (
        ('Macronutrient Breakdown', {
            'fields': (('protein_grams', 'calories'), ('carbs_grams', 'fats_grams'), 'fiber_grams')
        }),
        ('Ingredients & Allergens', {
            'fields': ('ingredients', 'allergen_info')
        }),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'display_order', 'image_preview')
    list_editable = ('is_active', 'display_order')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="40" style="object-fit:contain;" />', obj.image.url)
        return "-"
    image_preview.short_description = "Image"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'protein_grams', 'calories', 'is_active', 'is_featured', 'display_order')
    list_editable = ('is_active', 'is_featured', 'display_order')
    list_filter = ('category', 'is_active', 'is_featured')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, NutritionalProfileInline]
