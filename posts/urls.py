from django.urls import path
from django.conf.urls import url
from .import views
# from posts.views import HomeView
from posts.views import HomeView

app_name = 'posts'
urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r"^$", views.AllPosts.as_view(), name="all"),
    path('<slug><int:pk>.', views.detail, name='detail'),
    url(
        r"by/(?P<username>[-\w]+)/$",
        views.UserPosts.as_view(),
        name="for_user"
    ),
    url(
        r"by/(?P<username>[-\w]+)/(?P<pk>\d+)/$",
        views.SinglePost.as_view(),
        name="single"
    ),
     url(r'^user/(\w+)/$', views.profile, name='profile'),
         url(r'^profile/$', views.view_profile, name='view_profile'),
    url(r'^profile/(?P<pk>\d+)/$', views.view_profile, name='view_profile_with_pk'),

]    