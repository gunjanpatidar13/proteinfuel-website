from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from apps.users.models import User, CustomerProfile, Address

class AddressInline(admin.TabularInline):
    model = Address
    extra = 0
    fields = ('address_line_1', 'address_line_2', 'city', 'state', 'postal_code', 'address_type', 'is_default')


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'phone_number', 'user_type', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_active')
    search_fields = ('email', 'phone_number', 'first_name', 'last_name')
    ordering = ('email',)
    
    # Define custom fieldsets since username is removed
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number', 'user_type')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('collapse',),
            'fields': ('email', 'password', 'user_type', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'fitness_goal', 'loyalty_points', 'daily_protein_target')
    list_filter = ('fitness_goal',)
    search_fields = ('user__email', 'user__phone_number')
    inlines = [AddressInline]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('customer', 'address_line_1', 'city', 'address_type', 'is_default', 'is_deleted')
    list_filter = ('address_type', 'is_default', 'is_deleted')
    search_fields = ('customer__user__email', 'address_line_1', 'city', 'postal_code')
