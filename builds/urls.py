from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api$', views.api_root),
    url(r'^getting_started$', views.getting_started, name='getting-started'),
    url(r'^search$', views.search, name='search'),
    url(r'^react$', views.react, name='react'),
    url(r'^api/builds$', views.BuildsHandler.as_view(), name='build-list'),
    url(r'^api/builds/([0-9]+)$', views.BuildHandler.as_view(), name='build'),
    url(r'^api/components$', views.ComponentsHandler.as_view(), name='component-list'),
    url(r'^api/versions$', views.VersionsHandler.as_view(), name='version-list'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
