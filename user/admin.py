from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from crypto.models import FollowedCrypto

class FollowedCryptoInline(admin.TabularInline):
    model = FollowedCrypto
    extra = 0
    autocomplete_fields = ['crypto']
    verbose_name = "Followed Crypto"
    verbose_name_plural = "Followed Cryptos"


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    inlines = [FollowedCryptoInline]

    list_display = (
        'username', 'email', 'first_name', 'last_name',
        'phone_number', 'date_of_birth', 'gender',
        'is_writer',
        'is_staff',
    )

    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {
            "fields": (
                'phone_number', 'date_of_birth',
                'gender', 'profile_picture', 'short_bio',
                'is_writer',
            )
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {
            "fields": (
                'phone_number', 'date_of_birth',
                'gender', 'profile_picture', 'short_bio',
                'is_writer',
            )
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
