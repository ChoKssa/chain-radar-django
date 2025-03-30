from django.contrib import admin
from .models import Article, Paragraph

class ParagraphInline(admin.TabularInline):
    model = Paragraph
    extra = 1

class ArticleAdmin(admin.ModelAdmin):
    inlines = [ParagraphInline]
    list_display = ['title', 'author', 'created_at']
    search_fields = ['title', 'author__username']

admin.site.register(Article, ArticleAdmin)
admin.site.register(Paragraph)
