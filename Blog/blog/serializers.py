from rest_framework import serializers
from blog.models import Post
from django.contrib.auth.models import User


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='owner.author')
    class Meta:
        model = Post
        fields = ('author', 'title', 'text', 'id')


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, queryset=Post.objects.all())

    class Meta:
        model = User
        fields = ('id', 'author', 'posts')


class UserCreateSerializer(serializers.ModelSerializer):
    username = serializers.EmailField(label='Email')
    class Meta:
        model = User
        fields = ['username', 'password', ]
        extra_kwargs = {"password": {"write_only":True}}

    def create(self, validated_data):
        username = validated_data['username']
        #email = validated_data['email']
        password = validated_data['password']
        user_obj = User(username=username, password=password)
        user_obj.set_password(password)
        user_obj.save()
        return validated_data