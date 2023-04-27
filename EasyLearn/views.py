from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .permissions import IsOwnerOrReadOnly
from .serializers import EnrollmentSerializer, CourseSerializer, UserSerializer, BlocksSerializer
from .models import Enrollment, Course, LessonBlocks


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
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
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
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    def list(self, request, *args, **kwargs):
        user = request.user
        enrollments = Enrollment.objects.filter(user=user)
        courses = Course.objects.filter(author=user)
        enrollment_serializer = EnrollmentSerializer(enrollments, many=True)
        course_serializer = CourseSerializer(courses, many=True)
        data = {
            'enrollments': enrollment_serializer.data,
            'courses': course_serializer.data
        }

        return Response({'data': data})
