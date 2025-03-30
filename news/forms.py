from django import forms
from django.forms import inlineformset_factory
from .models import Article, Paragraph


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'thumbnail', 'video_url', 'introduction']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input'}),
            'introduction': forms.Textarea(attrs={'class': 'textarea', 'rows': 4}),
            'video_url': forms.URLInput(attrs={'class': 'input'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'input'}),
        }

class ParagraphForm(forms.ModelForm):
    class Meta:
        model = Paragraph
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input'}),
            'content': forms.Textarea(attrs={'class': 'textarea', 'rows': 3, 'resize': 'vertical'}),
        }

ParagraphFormSet = inlineformset_factory(
    Article,
    Paragraph,
    form=ParagraphForm,
    extra=1,
    can_delete=True
)
