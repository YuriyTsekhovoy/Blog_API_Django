#from django.http import 
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.db.models import Q
from blog.models import Post
from blog.serializers import PostSerializer, UserSerializer, UserCreateSerializer
from blog.permissions import IsOwnerOrReadOnly


class AllPostList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def dispatch(self, request, *args, **kwargs):
        self.query = request.GET.get('query')
        return super(AllPostList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Post.objects.all()
#        return Post.objects.all().filter(text__contains=self.query); Post.objects.all().filter(title__contains=self.query)
#        return Post.objects.all().exclude(text__contains=self.query, title__contains=self.query)
        if self.query:
            queryset = queryset.filter(Q(text__contains=self.query) | Q(title__contains=self.query))
        return queryset


class PostList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    search_fields = ('title', 'text')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user) 

    def get_queryset(self):
        user = self.request.user
        try:
            return Post.objects.filter(author=user)
        except TypeError:
            return Post.objects.all()


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreate(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()