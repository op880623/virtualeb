from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.list, name='url_list_all'),
    url(r'^(?P<category>\S+/)?(?P<id>[0-9]+)/(?:(?P<slug>\S+)/)?$', views.article, name='url_article'),
    url(r'^(?P<category>\S+/)$', views.list, name='url_list'),
]
