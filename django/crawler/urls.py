from django.urls import path

from . import views
from django.views import static
from django.conf import settings
from django.conf.urls import url

app_name = 'crawler'  # 设置命名空间
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('movies', views.show_movies, name='show_movies'),
    path('search', views.MoviesSearchView.as_view(), name='search'),
    url(r'^static/(?P<path>.*)$', static.serve,
        {'document_root': settings.STATIC_ROOT}, name='static'),
]
