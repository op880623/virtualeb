from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.urls import reverse
from django.core.paginator import Paginator
from .models import Article, Classification, Comment
from .forms import CommentForm
from django.http import HttpResponse
import re


def list(request, category=''):
    try:
        classification = Classification.objects.get(name__iregex=re.sub('-', '.', '^'+category.split('/')[-2]+'$'))
        if classification.format_url() == category:
            articles = Article.objects.filter(classification=classification).order_by('-created_date')
            list_name = classification.name
        else:
            return redirect(reverse('url_list', kwargs={'category': classification.format_url()}))
    except:
        if category:
            return redirect(reverse('url_list_all'))
        if request.GET.get('search'):
            # return HttpResponse(request.GET.get('search'))
            articles = Article.objects.filter(title__icontains=request.GET.get('search'))
            list_name = 'Search result'
        else:
            articles = Article.objects.order_by('-created_date')
            list_name = 'All articles'

    paginator = Paginator(articles, 10)
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except:
        articles = paginator.page(1)
    categories = get_list_or_404(Classification)

    return render(request, 'startbootstrap-blog-4-dev/list.html', {'list_name': list_name, 'articles': articles, 'categories': categories})

def article(request, id, slug='', category=''):
    article = get_object_or_404(Article, id=int(id))
    if slug == article.slug() and id == str(int(id)).zfill(5) and category == article.classification.format_url():
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
        return redirect(reverse('url_article', kwargs={'id': str(int(id)).zfill(5), 'slug': article.slug(), 'category': article.classification.format_url()}))
