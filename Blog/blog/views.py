# from django.http import
from django.contrib.auth.models import User
# from django.contrib.auth import get_user_model
from rest_framework import generics, permissions

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from django.db.models import Q
from blog.models import Post
from blog.serializers import (
    PostSerializer, UserSerializer, UserCreateSerializer, UserLoginSerializer)
from blog.permissions import IsOwnerOrReadOnly


class AllPostList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def dispatch(self, request, *args, **kwargs):
        self.query = request.GET.get('query')
        return super(AllPostList, self).dispatch(
            request, *args, **kwargs
        )

    def get_queryset(self):
        queryset = Post.objects.all()
        if self.query:
            queryset = queryset.filter(
                Q(text__icontains=self.query) |
                Q(title__icontains=self.query)
            )
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
    #permission_classes = AllowAny,
    permission_classes = (
                        permissions.IsAuthenticatedOrReadOnly,
                        IsOwnerOrReadOnly, 
                        #permissions.IsAdminUser,
                        )
    authentication_classes = (JSONWebTokenAuthentication, )
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser, )


class UserCreate(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny, )


class UserLogin(APIView):
    permission_classes = (AllowAny, )
    serializer_class = UserLoginSerializer

    def post (self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)