from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampedModel, SoftDeleteModel

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    user_type = models.CharField(
        max_length=20,
        choices=(
            ('CUSTOMER', 'Customer'),
            ('STAFF', 'Staff'),
            ('ADMIN', 'Admin')
        ),
        default='CUSTOMER'
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class CustomerProfile(TimeStampedModel):
    GOAL_CHOICES = (
        ('BULK', 'Muscle Gain / Bulk'),
        ('CUT', 'Fat Loss / Cut'),
        ('MAINTAIN', 'Weight Maintenance'),
        ('HEALTHY', 'General Healthy Eating'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer_profile")
    loyalty_points = models.IntegerField(default=0)
    fitness_goal = models.CharField(max_length=20, choices=GOAL_CHOICES, default='HEALTHY')
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    daily_protein_target = models.PositiveIntegerField(default=100, help_text="in grams")

    def __str__(self):
        return f"Profile - {self.user.email}"


class Address(TimeStampedModel, SoftDeleteModel):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name="addresses")
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, default="Bangalore")
    state = models.CharField(max_length=100, default="Karnataka")
    postal_code = models.CharField(max_length=20)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    address_type = models.CharField(
        max_length=20,
        choices=(('HOME', 'Home'), ('WORK', 'Work'), ('OTHER', 'Other')),
        default='HOME'
    )
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f"{self.address_line_1}, {self.city} ({self.address_type})"

    def save(self, *args, **kwargs):
        if self.is_default:
            # Set other addresses of this customer to is_default = False
            Address.objects.filter(customer=self.customer, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)
