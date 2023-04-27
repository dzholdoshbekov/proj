from django.db import models
from django.contrib.auth.models import User
from django.db.models import PROTECT


class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_courses', null=True)
    students = models.ManyToManyField(User, through='Enrollment', related_name='enrolled_courses')
    price = models.IntegerField(null=True)
    discount = models.IntegerField(null=True)
    cat = models.ForeignKey('Category', related_name="Категории", on_delete=PROTECT, null=True)

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} enrolled in {self.course.title}'


class LessonBlocks(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    course = models.ForeignKey('Course', related_name="БлокиКурса", on_delete=PROTECT, null=True, blank=True)
