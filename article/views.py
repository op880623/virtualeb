from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.urls import reverse
from django.core.paginator import Paginator
from .models import Article, Classification, Comment
from .forms import CommentForm
import re


def list_redirect(request, category):
    return redirect(reverse('url_list', kwargs={'category': category}))

def list(request, category):
    classification = get_object_or_404(Classification, name__iregex=re.sub('-', '.', '^'+category.split('/')[-2]+'$'))
    if classification.format_url() == category:
        articles = Article.objects.filter(classification=classification)
        paginator = Paginator(articles, 10)
        page = request.GET.get('page')
        try:
            articles = paginator.page(page)
        except:
            articles = paginator.page(1)
        children = classification.list_child()
        categories = get_list_or_404(Classification)
        return render(request, 'startbootstrap-blog-4-dev/list.html', {'list_name': classification.name, 'children': children, 'articles': articles, 'categories': categories})
    else:
        return redirect(reverse('url_list_redirect', kwargs={'category': classification.format_url()}))

def list_all(request):
    articles = Article.objects.all()
    paginator = Paginator(articles, 10)
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except:
        articles = paginator.page(1)
    categories = get_list_or_404(Classification)
    return render(request, 'startbootstrap-blog-4-dev/list.html', {'list_name': 'All articles', 'articles': articles, 'categories': categories})

def article_redirect(request, id):
    article = get_object_or_404(Article, id=int(id))
    return redirect(reverse('url_article', kwargs={'id': str(int(id)).zfill(5), 'slug': article.slug(), 'category': article.classification.format_url()[:-1]}))

def article(request, id, slug='', category=''):
    article = get_object_or_404(Article, id=int(id))
    if slug == article.slug() and id == str(int(id)).zfill(5) and category == article.classification.format_url()[:-1]:
        if request.method == 'POST':
            if CommentForm(request.POST).is_valid():
                form = CommentForm(request.POST)
                comment = form.save(commit=False)
                comment.belong_to=article
                comment.save()
        form = CommentForm()
        comments = Comment.objects.filter(belong_to=article).order_by('comment_date')
        categories = get_list_or_404(Classification)
        return render(request, 'startbootstrap-blog-4-dev/article.html',  {'article': article, 'form': form, 'comments': comments, 'categories': categories})
    else:
        return redirect(reverse('url_article_redirect', kwargs={'id': str(int(id)).zfill(5)}))
