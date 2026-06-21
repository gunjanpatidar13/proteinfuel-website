from django.db import models
from django.utils import timezone
from apps.core.utils import compress_image

class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        return super().update(is_deleted=True, deleted_at=timezone.now())

    def hard_delete(self):
        return super().delete()

class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(is_deleted=False)

class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(using=using)

    def hard_delete(self, using=None, keep_parents=False):
        super().delete(using=using, keep_parents=keep_parents)


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class SiteSettings(SingletonModel, TimeStampedModel):
    site_name = models.CharField(max_length=100, default="ProteinFuel")
    logo = models.ImageField(upload_to="settings/", null=True, blank=True)
    logo_dark = models.ImageField(upload_to="settings/", null=True, blank=True)
    contact_email = models.EmailField(default="info@proteinfuel.com")
    contact_phone = models.CharField(max_length=20, default="+91 99999 99999")
    contact_address = models.TextField(default="Bangalore, India")
    footer_about = models.TextField(blank=True, default="ProteinFuel sells high protein waffles, shakes, coffees, and snacks to keep you active and fueled.")
    copyright_text = models.CharField(max_length=200, default="© 2026 ProteinFuel. All rights reserved.")
    google_analytics_id = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., G-XXXXXXX")
    meta_title = models.CharField(max_length=100, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    robots_txt = models.TextField(blank=True, null=True, default="User-agent: *\nAllow: /")
    sitemap_xml = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Site Settings"

    def save(self, *args, **kwargs):
        # Image compression
        if self.logo:
            try:
                this = SiteSettings.objects.get(pk=self.pk)
                if this.logo != self.logo:
                    self.logo = compress_image(self.logo, max_width=400)
            except SiteSettings.DoesNotExist:
                self.logo = compress_image(self.logo, max_width=400)

        if self.logo_dark:
            try:
                this = SiteSettings.objects.get(pk=self.pk)
                if this.logo_dark != self.logo_dark:
                    self.logo_dark = compress_image(self.logo_dark, max_width=400)
            except SiteSettings.DoesNotExist:
                self.logo_dark = compress_image(self.logo_dark, max_width=400)
        super().save(*args, **kwargs)


class HomepageContent(SingletonModel, TimeStampedModel):
    hero_headline = models.CharField(max_length=200, default="Fuel Your Day With Protein")
    hero_subheadline = models.CharField(max_length=300, default="High Protein Waffles, Shakes & Coffee Delivered Fresh")
    hero_button_text = models.CharField(max_length=50, default="Order Now")
    hero_button_url = models.CharField(max_length=200, default="/products/")
    hero_image = models.ImageField(upload_to="homepage/", null=True, blank=True)

    why_choose_title = models.CharField(max_length=200, default="Why Choose ProteinFuel")
    why_choose_subtitle = models.CharField(max_length=300, default="We blend premium protein with delicious recipes.")

    nutrition_title = models.CharField(max_length=200, default="Our Nutrition Philosophy")
    nutrition_content = models.TextField(default="Protein is the building block of life...")

    cta_title = models.CharField(max_length=200, default="Start Your Protein Journey Today")
    cta_subtitle = models.CharField(max_length=300, default="Fuel your gains with our high protein menu items.")
    cta_button_text = models.CharField(max_length=50, default="Explore Menu")
    cta_button_url = models.CharField(max_length=200, default="/products/")

    class Meta:
        verbose_name = "Homepage Content"
        verbose_name_plural = "Homepage Content"

    def __str__(self):
        return "Homepage Content"

    def save(self, *args, **kwargs):
        if self.hero_image:
            try:
                this = HomepageContent.objects.get(pk=self.pk)
                if this.hero_image != self.hero_image:
                    self.hero_image = compress_image(self.hero_image, max_width=1200)
            except HomepageContent.DoesNotExist:
                self.hero_image = compress_image(self.hero_image, max_width=1200)
        super().save(*args, **kwargs)


class WhyChooseItem(TimeStampedModel):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon_name = models.CharField(max_length=50, help_text="Bootstrap icon class name, e.g., 'lightning-fill'")
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'id']
        verbose_name = "Why Choose Card"
        verbose_name_plural = "Why Choose Cards"

    def __str__(self):
        return self.title


class Testimonial(TimeStampedModel):
    customer_name = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField(default=5)
    review_text = models.TextField()
    customer_image = models.ImageField(upload_to="testimonials/", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return f"{self.customer_name} - {self.rating} Stars"

    def save(self, *args, **kwargs):
        if self.customer_image:
            try:
                this = Testimonial.objects.get(pk=self.pk)
                if this.customer_image != self.customer_image:
                    self.customer_image = compress_image(self.customer_image, max_width=200)
            except Testimonial.DoesNotExist:
                self.customer_image = compress_image(self.customer_image, max_width=200)
        super().save(*args, **kwargs)


class GalleryItem(TimeStampedModel):
    image = models.ImageField(upload_to="gallery/")
    title = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return self.title or f"Gallery Item {self.id}"

    def save(self, *args, **kwargs):
        if self.image:
            try:
                this = GalleryItem.objects.get(pk=self.pk)
                if this.image != self.image:
                    self.image = compress_image(self.image, max_width=800)
            except GalleryItem.DoesNotExist:
                self.image = compress_image(self.image, max_width=800)
        super().save(*args, **kwargs)


class FAQ(TimeStampedModel):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'id']
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question


class ContactInquiry(TimeStampedModel):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Contact Inquiry"
        verbose_name_plural = "Contact Inquiries"
        ordering = ['-created_at']

    def __str__(self):
        return f"Inquiry from {self.name} ({self.email})"


class FranchiseApplication(TimeStampedModel):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    city = models.CharField(max_length=100)
    investment_budget = models.CharField(max_length=100, help_text="e.g. 10-20 Lakhs, 20-50 Lakhs")
    message = models.TextField()
    is_reviewed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Franchise App from {self.name} ({self.city})"


class Job(TimeStampedModel, SoftDeleteModel):
    STATUS_CHOICES = (
        ('ACTIVE', 'Active / Hiring'),
        ('CLOSED', 'Closed'),
    )
    position = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()  # Will use CKEditor widget in admin
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.position} - {self.location} ({self.status})"


class JobApplication(TimeStampedModel):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    resume = models.FileField(upload_to="resumes/")
    cover_letter = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Application for {self.job.position} by {self.name}"


class StatCard(TimeStampedModel):
    value = models.CharField(max_length=50, help_text="e.g. 10000+, 50+")
    label = models.CharField(max_length=100, help_text="e.g. Happy Customers, Cities Reached")
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'id']

    def __str__(self):
        return f"{self.value} - {self.label}"


class SocialLink(TimeStampedModel):
    platform_name = models.CharField(max_length=50, help_text="e.g. Instagram, Facebook, Twitter")
    url = models.URLField()
    icon_name = models.CharField(max_length=50, help_text="Bootstrap icon class name, e.g. 'instagram'")
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'id']

    def __str__(self):
        return self.platform_name


class NewsletterSubscriber(TimeStampedModel):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.email
