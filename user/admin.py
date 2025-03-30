from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
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
