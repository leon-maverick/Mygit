from django.conf.urls import url, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'music'

urlpatterns = [
    # /music/
    url(r'^$', views.IndexView.as_view(), name='index'),

    url(r'^register/$', views.UserFormView.as_view(), name='register'),

    url(r'^login/$', views.UserFormLogin.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^boxcars/$', views.BoxcarsView.as_view(), name='Boxcars'),

    # game page
    #url(r'^games/$', views.GamesView.as_view(), name='games'),
    url(r'^games/$', views.GameList.as_view(), name='games'),

    # /music/album_id/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

    # music/album/add
    url(r'^album/add/$', views.AlbumCreate.as_view(), name='album-add'),

    # music/album/2
    url(r'^album/(?P<pk>[0-9]+)/$', views.AlbumUpdate.as_view(), name='album-update'),

    # music/album/2/delete
    url(r'^album/(?P<pk>[0-9]+)/delete$', views.AlbumDelete.as_view(), name='album-delete'),

    # /music/album_id/favorite
   # url(r'^(?P<album_id>[0-9]+)/favorite$', views.favorite, name='favorite'),

]

#urlpatterns = format_suffix_patterns(urlpatterns)