
from django.contrib import admin
from django.urls import path, include, re_path


from rest_framework import routers

from EasyLearn.views import *

router = routers.DefaultRouter()
router.register(r'course', CourseViewSet)
router.register(r'enrollments', EnrollmentViewSet, basename='enrollments')
router.register(r'my-account', MyAccountView, basename='my-account')
router.register(r'users', UserViewSet, basename='user')
router.register(r'course/(?P<course_pk>[^/.]+)/block', CourseBlockViewSet, basename='course-block')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]