from rest_framework import serializers
from rest_framework.serializers import (ModelSerializer, ValidationError)

from blog.models import Post
from django.contrib.auth.models import User


class PostSerializer(ModelSerializer):
    #author = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Post
        fields = ('author', 'title', 'text', 'id', 'created_date', )


class UserSerializer(ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Post.objects.all())

    class Meta:
        model = User
        fields = ('id', 'author', 'posts')


class UserCreateSerializer(ModelSerializer):
    username = serializers.EmailField(label='Email')

    class Meta:
        model = User
        fields = ('username', 'password', )
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        username = data['username']
        user_qs = User.objects.filter(username=username)
        if user_qs.exists():
            raise ValidationError("This user has already registered.")
        return data

    def create(self, validated_data):
        username = validated_data['username']
        #email = validated_data['email']
        password = validated_data['password']
        user_obj = User(username=username, password=password)
        user_obj.set_password(password)
        user_obj.save()
        return validated_data


class UserLoginSerializer(ModelSerializer):
    token = serializers.CharField(allow_blank=True, read_only=True)
    username = serializers.EmailField(label='Email', allow_blank=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'token')
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        user_obj = None
        username = data.get('username', None)
        password = data["password"]
        if not username:
            raise ValidationError("The e-mail required to login")

        user = User.objects.filter(username=username).distinct()
        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError("This e-mail is not valid.")

        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Incorrect password, please try again.")

        #data["token"] = "SOME RANDOM TOKEN"
        return data
   # def create(self, validated_data):
   #     username = validated_data['username']
   #     #email = validated_data['email']
   #     password = validated_data['password']
   #     user_obj = User(username=username, password=password)
   #     user_obj.set_password(password)
   #     user_obj.save()
   #     return validated_data
