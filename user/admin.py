from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from crypto.models import FollowedCrypto

# Inline admin to manage followed cryptocurrencies directly within the user admin panel
class FollowedCryptoInline(admin.TabularInline):
    model = FollowedCrypto
    extra = 0
    autocomplete_fields = ['crypto']
    verbose_name = "Followed Crypto"
    verbose_name_plural = "Followed Cryptos"

# Custom admin configuration for the CustomUser model
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    inlines = [FollowedCryptoInline]

    # Columns displayed in the user list view
    list_display = (
        'username', 'email', 'first_name', 'last_name',
        'phone_number', 'date_of_birth', 'gender',
        'is_writer',
        'is_staff',
    )

    # Additional fields to display in the user form (read/update)
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {
            "fields": (
                'phone_number', 'date_of_birth',
                'gender', 'profile_picture', 'short_bio',
                'is_writer',
            )
        }),
    )

    # Fields to display when adding a new user
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {
            "fields": (
                'phone_number', 'date_of_birth',
                'gender', 'profile_picture', 'short_bio',
                'is_writer',
            )
        }),
    )

# Register the customized user model with its admin interface
admin.site.register(CustomUser, CustomUserAdmin)
