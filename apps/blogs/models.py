from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from ckeditor.fields import RichTextField
from apps.core.models import TimeStampedModel, SoftDeleteModel
from apps.core.utils import compress_image

class BlogCategory(TimeStampedModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BlogTag(TimeStampedModel):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name = "Blog Tag"
        verbose_name_plural = "Blog Tags"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BlogPost(TimeStampedModel, SoftDeleteModel):
    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('PUBLISHED', 'Published'),
    )
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, related_name="posts")
    tags = models.ManyToManyField(BlogTag, blank=True, related_name="posts")
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    featured_image = models.ImageField(upload_to="blog/")
    content = RichTextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='DRAFT')
    published_at = models.DateTimeField(null=True, blank=True)

    # SEO Meta Fields
    meta_title = models.CharField(max_length=100, blank=True, null=True, help_text="For Google Search title")
    meta_description = models.TextField(blank=True, null=True, help_text="For Google Search snippet")

    class Meta:
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.status == 'PUBLISHED' and not self.published_at:
            self.published_at = timezone.now()
        if self.featured_image:
            try:
                this = BlogPost.objects.get(pk=self.pk)
                if this.featured_image != self.featured_image:
                    self.featured_image = compress_image(self.featured_image, max_width=1000)
            except BlogPost.DoesNotExist:
                self.featured_image = compress_image(self.featured_image, max_width=1000)
        super().save(*args, **kwargs)
