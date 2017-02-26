from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^$', views.api_root),
    url(r'^builds$', views.BuildsHandler.as_view(), name='build-list'),
    url(r'^builds/([0-9]+)$', views.BuildHandler.as_view()),
    url(r'^components$', views.ComponentsHandler.as_view(), name='component-list'),
    url(r'^versions$', views.VersionsHandler.as_view(), name='version-list'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
