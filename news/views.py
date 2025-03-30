from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.template.loader import render_to_string
from .models import Article
from .forms import ArticleForm, ParagraphFormSet

@login_required
def article_create(request):
    if not request.user.is_writer:
        return HttpResponseForbidden("You are not allowed to create articles.")

    article = Article(author=request.user)
    prefix = 'paragraph_set'

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        formset = ParagraphFormSet(request.POST, instance=article, prefix=prefix)
    else:
        form = ArticleForm(instance=article)
        formset = ParagraphFormSet(instance=article, prefix=prefix)

    empty_form = formset.empty_form
    empty_form.prefix = f'{prefix}-__prefix__'

    empty_form_html = render_to_string('news/partials/paragraph_form.html', {
        'form': empty_form,
    })

    if request.method == 'POST' and form.is_valid() and formset.is_valid():
        form.save()
        for i, paragraph_form in enumerate(formset.forms):
            if paragraph_form.cleaned_data and not paragraph_form.cleaned_data.get('DELETE', False):
                paragraph = paragraph_form.save(commit=False)
                paragraph.order = i
                paragraph.article = article
                paragraph.save()
        return redirect('article_detail', pk=article.pk)

    return render(request, 'news/article_create.html', {
        'form': form,
        'formset': formset,
        'empty_form_html': empty_form_html,
    })


@login_required
def article_update(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if request.user != article.author and not request.user.is_superuser:
        return HttpResponseForbidden("You are not allowed to edit this article.")

    prefix = "paragraphs"

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        formset = ParagraphFormSet(request.POST, instance=article, prefix=prefix)

        if form.is_valid() and formset.is_valid():
            form.save()
            for i, paragraph_form in enumerate(formset.forms):
                if paragraph_form.cleaned_data.get('DELETE', False):
                    if paragraph_form.instance.pk:
                        paragraph_form.instance.delete()
                else:
                    paragraph = paragraph_form.save(commit=False)
                    paragraph.order = i
                    paragraph.article = article
                    paragraph.save()
            return redirect('article_detail', pk=article.pk)
        else:
            print("Form errors:", form.errors)
            print("Formset errors:", formset.errors)
    else:
        form = ArticleForm(instance=article)
        formset = ParagraphFormSet(instance=article, prefix=prefix)

    empty_form = ParagraphFormSet(prefix=prefix).empty_form
    empty_form.prefix = f"{prefix}-__prefix__"
    empty_form_html = render_to_string('news/partials/paragraph_form.html', {
        'form': empty_form
    })

    return render(request, 'news/article_update.html', {
        'form': form,
        'formset': formset,
        'empty_form_html': empty_form_html,
        'article': article,
    })


@login_required
def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if article.author != request.user:
        return HttpResponseForbidden("You can only delete your own articles.")

    if request.method == 'POST':
        article.delete()
        return redirect('article_list')


def article_list(request):
    articles = Article.objects.all().order_by('-created_at')
    return render(request, 'news/articles.html', {'articles': articles})


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    paragraphs = article.paragraphs.order_by('order')
    return render(request, 'news/article_detail.html', {
        'article': article,
        'paragraphs': paragraphs,
    })
