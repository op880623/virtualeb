from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.urls import reverse
from .models import Article, Classification, Comment
from .forms import CommentForm
from django.http import HttpResponse


def list_by_category(request, category=''):
    try:
        classification = Classification.objects.get(name=category.split('/')[-1])
        articles = Article.objects.filter(classification=classification)
        children = classification.list_child()
    except:
        classification = ''
        articles = Article.objects.filter(classification__isnull=True)
        children = Classification.objects.filter(parent__isnull=True)
    return render(request, 'startbootstrap-blog-4-dev/list.html', {'category': classification, 'children': children, 'articles': articles})

def article_by_id(request, id):
    article = get_object_or_404(Article, id=int(id))
    return redirect(reverse('url_with_id_slug_category', kwargs={'id': str(int(id)).zfill(5), 'slug': article.slug(), 'category': article.classification.format_url()[:-1]}))

def article_by_category_id_slug(request, id, slug='', category=''):
    article = get_object_or_404(Article, id=int(id))

    if slug == article.slug() and id == str(int(id)).zfill(5) and category == article.classification.format_url()[:-1]:
        if request.method == 'POST':
            if CommentForm(request.POST).is_valid():
                form = CommentForm(request.POST)
                comment = form.save()
                comment.belong_to=article
                comment.save()
        form = CommentForm()
        comments = Comment.objects.filter(belong_to=article).order_by('comment_date')
        return render(request, 'startbootstrap-blog-4-dev/article.html',  {'article': article, 'contents': article.context(), 'form': form, 'comments': comments})
    else:
        return redirect(reverse('url_with_id', kwargs={'id': str(int(id)).zfill(5)}))
