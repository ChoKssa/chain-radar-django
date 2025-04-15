from django.utils.html import format_html
from django.contrib import admin
from .models import CryptoCurrency, CryptoSnapshot

# Admin configuration for the CryptoCurrency model
@admin.register(CryptoCurrency)
class CryptoCurrencyAdmin(admin.ModelAdmin):
    # Fields to display in the list view of the admin panel
    list_display = ('name', 'symbol', 'logo_preview')
    # Enable search functionality on name and symbol
    search_fields = ('name', 'symbol')
    # Order results by name
    ordering = ('name',)
    # Make the logo preview read-only
    readonly_fields = ('logo_preview',)

    def logo_preview(self, obj):
        # If the logo exists, render it as an image in the admin panel
        if obj.logo:
            return format_html('<img src="{}" width="40" height="40" style="object-fit: contain;" />', obj.logo.url)
        # Otherwise, return a placeholder text
        return "No logo"
    logo_preview.short_description = "Logo"  # Label shown in the admin panel

# Admin configuration for the CryptoSnapshot model
@admin.register(CryptoSnapshot)
class CryptoSnapshotAdmin(admin.ModelAdmin):
    # Fields to display in the list view of the admin panel
    list_display = ('crypto', 'timestamp', 'price', 'change_24h', 'market_cap', 'volume_24h')
    # Add a filter sidebar by crypto
    list_filter = ('crypto',)
    # Enable search functionality on related crypto name and symbol
    search_fields = ('crypto__name', 'crypto__symbol')
    # Order results by most recent snapshot first
    ordering = ('-timestamp',)
