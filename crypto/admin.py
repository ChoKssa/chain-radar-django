from django.utils.html import format_html
from django.contrib import admin
from .models import CryptoCurrency, CryptoSnapshot

@admin.register(CryptoCurrency)
class CryptoCurrencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'logo_preview')
    search_fields = ('name', 'symbol')
    ordering = ('name',)
    readonly_fields = ('logo_preview',)

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="40" height="40" style="object-fit: contain;" />', obj.logo.url)
        return "No logo"
    logo_preview.short_description = "Logo"

@admin.register(CryptoSnapshot)
class CryptoSnapshotAdmin(admin.ModelAdmin):
    list_display = ('crypto', 'timestamp', 'price', 'change_24h', 'market_cap', 'volume_24h')
    list_filter = ('crypto',)
    search_fields = ('crypto__name', 'crypto__symbol')
    ordering = ('-timestamp',)
