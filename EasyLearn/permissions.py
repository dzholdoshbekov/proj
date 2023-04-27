from django.db.migrations import serializer
from requests import Response
from rest_framework import permissions, request
from rest_framework.generics import get_object_or_404

from .models import Course, User


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True


        return obj.author == request.user


class IsLessonBlockAuthor(permissions.BasePermission):
    """
    Custom permission to only allow lesson block authors to add, update, or delete the block.
    """
    def has_permission(self, request, view):
        # Check if the request method is safe (GET, HEAD, OPTIONS
        # else:
        #     return Response(serializer.errors, status=400)



        # Otherwise, check if the user is the author of the course that the block belongs to
        course_id = view.kwargs.get('course_pk')
        course = Course.objects.get(pk=course_id)
        return course.author == request.user
