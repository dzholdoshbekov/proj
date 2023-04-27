from collections import OrderedDict

from django.contrib.auth.models import User


from .serializers import UserSerializer, CourseSerializer, EnrollmentSerializer
from rest_framework import viewsets, permissions, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response


from .permissions import *
from .serializers import *



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CourseBlockViewSet(viewsets.ModelViewSet):
    queryset = LessonBlocks.objects.all()
    serializer_class = BlocksSerializer

    def get_permissions(self):
        if self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [permissions.IsAuthenticated, IsLessonBlockAuthor]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated, IsLessonBlockAuthor]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class MyAccountView(viewsets.ModelViewSet):
    serializer_class = EnrollmentSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user
        return Enrollment.objects.filter(user=user)

    def list(self, request):
        user = self.request.user
        enrolled_courses = Enrollment.objects.filter(user=user)
        authored_courses = Course.objects.filter(author=user)
        enrolled_serializer = EnrollmentSerializer(enrolled_courses, many=True)
        authored_serializer = CourseSerializer(authored_courses, many=True)

        return Response({
            'enrolled_courses', enrolled_serializer.data,
            'authored_courses', authored_serializer.data
        })