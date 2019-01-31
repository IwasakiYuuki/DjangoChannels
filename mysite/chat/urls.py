from django.conf.urls import url

from . import views


app_name = 'chat'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create_user/$', views.create_user, name='create_user'),
    url(r'^room/$', views.room, name='room'),
]