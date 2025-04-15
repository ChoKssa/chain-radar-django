from django.contrib import admin
from .models import Article, Paragraph

# Allows inline editing of Paragraphs within the Article admin page
class ParagraphInline(admin.TabularInline):
    model = Paragraph
    extra = 1

# Custom admin configuration for the Article model
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ParagraphInline]
    list_display = ['title', 'author', 'created_at']
    search_fields = ['title', 'author__username']

# Register Article model with its custom admin interface
admin.site.register(Article, ArticleAdmin)
# Register Paragraph model with default admin interface
admin.site.register(Paragraph)
