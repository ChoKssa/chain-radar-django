from django.db import models
from django.conf import settings

class Article(models.Model):
    title = models.CharField(max_length=255)
    introduction = models.TextField()
    thumbnail = models.ImageField(upload_to="article_thumbnails/", null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='articles'
    )

    def __str__(self):
        return self.title

    def can_edit(self, user):
        return self.author == user


class Paragraph(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='paragraphs')
    title = models.CharField(max_length=255)
    content = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
