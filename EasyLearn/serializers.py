from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class CourseSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    final_price = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ('title', 'description', 'cat', 'author', 'price', 'discount', 'final_price')

    def get_final_price(self, obj):
        discount = obj.discount
        price = obj.price
        final_price = price - (price * (discount / 100))
        return final_price


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']


class BlocksSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonBlocks
        fields = ['title', 'body']


class EnrollmentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Enrollment
        fields = ('user', 'course', 'date_joined')

