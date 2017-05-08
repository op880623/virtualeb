from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.list_all, name='url_list'),
    url(r'^(?P<id>[0-9]+)/$', views.article_redirect, name='url_article_redirect'),
    url(r'^(?:(?P<category>\S+)/)?(?P<id>[0-9]+)/(?:(?P<slug>\S+)/)?$', views.article, name='url_article'),
    url(r'^(?P<category>.+)$', views.list, name='url_list'),
    url(r'^(?P<category>.+)$', views.list_redirect, name='url_list_redirect'),
]
