from django.conf.urls import url

from . import views


app_name = 'chat'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create_user/$', views.create_user, name='create_user'),
    url(r'^room/$', views.room, name='room'),
#    url(r'^test/$', views.test, name='test'),
#    url(r'^auth/$', views.auth, name='auth'),
#    url(r'^callback/$', views.callback, name='callback'),
]