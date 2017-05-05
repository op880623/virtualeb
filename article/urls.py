from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.list_by_category, name='url_list'),
    url(r'^(?P<id>[0-9]+)/$', views.article_by_id, name='url_with_id'),
    url(r'^(?:(?P<category>\S+)/)?(?P<id>[0-9]+)/(?:(?P<slug>\S+)/)?$', views.article_by_category_id_slug, name='url_with_id_slug_category'),
    url(r'^(?P<category>\S+)/$', views.list_by_category, name='url_with_category'),
]
