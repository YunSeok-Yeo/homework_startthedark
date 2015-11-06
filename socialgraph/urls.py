from django.conf.urls import include, url
from socialgraph import views
urlpatterns = [
    url(r'^followers/(?P<username>[a-zA-Z0-9_-]+)/$', views.friend_list, {'list_type':'followers'}, name='sg_followers'),
    url(r'^following/(?P<username>[a-zA-Z0-9_-]+)/$', views.friend_list, {'list_type':'following'}, name='sg_following'),
    url(r'^mutual/(?P<username>[a-zA-Z0-9_-]+)/$', views.friend_list, {'list_type':'mutal'}, name='sg_mutal'),    
]
