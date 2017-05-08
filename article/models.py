from datetime import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify


class Classification(models.Model):
    name = models.CharField(max_length=200)
    parent = models.ForeignKey('self', blank=True, null=True)

    def slug(self):
        return slugify(self.name, allow_unicode=True)

    def list_child(self):
        return Classification.objects.filter(parent=self)

    def list_offspring(self):
        offspring = self.list_child()
        for child in self.list_child():
            offspring = offspring.union(child.list_offspring())
        return offspring

    def list_article(self):
        return Article.objects.filter(classification=self)

    def list_all_article(self):
        all_article = self.list_article()
        for child in self.list_child():
            all_article = all_article.union(child.list_all_article())
        return all_article

    def format_url(self):
        if self.parent:
            return self.parent.format_url() + self.slug() + '/'
        else:
            return self.slug() + '/'

    def __str__(self):
        return self.name


class Article(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    classification = models.ForeignKey(Classification)
    source = models.URLField(max_length=200, blank=True, null=True)

    def slug(self):
        return slugify(self.title, allow_unicode=True)

    def context(self):
        return Content.objects.filter(belong_to=self).get(previous_content__isnull=True).catenate()

    def update(self):
        self.updated_date = timezone.now()
        self.save()

    def list_sibling(self):
        return self.classification.list_article()

    def format_simple_url(self):
        return str(self.id)+'/'+self.slug()+'/'

    def format_url(self):
        if self.classification:
            return self.classification.format_url()+self.format_simple_url()
        else:
            return self.format_simple_url()

    def __str__(self):
        return self.title



class Content(models.Model):
    belong_to = models.ForeignKey(Article, related_name='content')
    previous_content = models.ForeignKey('self', blank=True, null=True, related_name='previous')

    h1 = '1'
    h2 = '2'
    h3 = '3'
    h4 = '4'
    h5 = '5'
    h6 = '6'
    a = '7'
    p = '8'
    img = '9'
    HTML_TAG = (
        (h1, 'h1'),
        (h2, 'h2'),
        (h3, 'h3'),
        (h4, 'h4'),
        (h5, 'h5'),
        (h6, 'h6'),
        (a, 'a'),
        (p, 'p'),
        (img, 'img'),
    )
    html_tag = models.CharField(max_length = 1, choices = HTML_TAG, default = p)

    text = models.TextField(default = "new content")
    html_class = models.CharField(max_length=200, blank=True, null=True)
    href = models.CharField(max_length=200, blank=True, null=True)
    src = models.CharField(max_length=200, blank=True, null=True)
    alt = models.CharField(max_length=200, blank=True, null=True)

    def catenate(self):
        content_seq = [self]
        try:
            content_seq = content_seq + Content.objects.get(previous_content=self).catenate()
        except:
            pass
        return content_seq

    def __str__(self):
        return self.text[:20]


class Comment(models.Model):
    belong_to = models.ForeignKey(Article)
    comment_on = models.ForeignKey('self', blank=True, null=True)

    commenter = models.CharField(max_length=60)
    text = models.TextField()
    comment_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.comment_date.strftime('%y/%m/%d %H:%M:%S')
