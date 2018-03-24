from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_jwt.views import obtain_jwt_token
from blog import views

urlpatterns = [
    # url(r'^posts/$', views.PostList.as_view()),
    url(r'^api/auth/login/$', views.UserLogin.as_view(), name='login'),
    url(r'^api/auth/register/$', views.UserCreate.as_view(), name='register'),
    url(r'^api/posts/$', views.AllPostList.as_view()),
    url(r'^api/me/posts/$', views.PostList.as_view()),
    url(r'^api/me/posts/(?P<pk>[0-9]+)/$', views.PostDetail.as_view()),

    url(r'^api/auth/token/', obtain_jwt_token),
]
