from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^posts/$', views.PostList.as_view()),
]