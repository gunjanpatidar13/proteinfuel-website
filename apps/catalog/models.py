from django.db import models
from django.utils.text import slugify
from apps.core.models import TimeStampedModel, SoftDeleteModel
from apps.core.utils import compress_image

class Category(TimeStampedModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="categories/", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if self.image:
            try:
                this = Category.objects.get(pk=self.pk)
                if this.image != self.image:
                    self.image = compress_image(self.image, max_width=400)
            except Category.DoesNotExist:
                self.image = compress_image(self.image, max_width=400)
        super().save(*args, **kwargs)


class Product(TimeStampedModel, SoftDeleteModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    protein_grams = models.PositiveIntegerField(help_text="Protein in grams")
    calories = models.PositiveIntegerField(help_text="Calories in kcal")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def primary_image(self):
        primary = self.images.filter(is_primary=True).first()
        if not primary:
            primary = self.images.first()
        return primary.image if primary else None


class ProductImage(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/")
    is_primary = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'id']

    def __str__(self):
        return f"Image for {self.product.name}"

    def save(self, *args, **kwargs):
        if self.is_primary:
            # Set other images of this product to is_primary = False
            ProductImage.objects.filter(product=self.product, is_primary=True).update(is_primary=False)
        if self.image:
            try:
                this = ProductImage.objects.get(pk=self.pk)
                if this.image != self.image:
                    self.image = compress_image(self.image, max_width=800)
            except ProductImage.DoesNotExist:
                self.image = compress_image(self.image, max_width=800)
        super().save(*args, **kwargs)


class NutritionalProfile(TimeStampedModel):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="nutrition_profile")
    calories = models.PositiveIntegerField(help_text="Calories in kcal")
    protein_grams = models.PositiveIntegerField(help_text="Protein in grams")
    carbs_grams = models.PositiveIntegerField(help_text="Carbohydrates in grams")
    fats_grams = models.PositiveIntegerField(help_text="Fats in grams")
    fiber_grams = models.PositiveIntegerField(default=0, help_text="Dietary Fiber in grams")
    ingredients = models.TextField(help_text="Comma-separated or paragraph list of ingredients")
    allergen_info = models.CharField(max_length=255, blank=True, null=True, help_text="e.g. Contains Milk, Soy, Gluten")

    def __str__(self):
        return f"Nutrition - {self.product.name}"
