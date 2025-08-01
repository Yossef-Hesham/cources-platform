from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
        # ('admin', 'Admin'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    biography = models.TextField(max_length=1000, blank=False, null=True)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    national_id = models.CharField(max_length=14)
    photo = models.ImageField(upload_to='students/photos/', null=True, blank=True)
    date_of_birth = models.DateField()
    grade = models.IntegerField(null=True, blank=True)

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    national_id = models.CharField(max_length=14)
    photo = models.ImageField(upload_to='teachers/photos/', null=True, blank=True)
    date_of_birth = models.DateField()
    rate = models.FloatField(default=0, null=False, blank=True)
    biography = models.TextField(max_length=1000, blank=False, null=True)

class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)


class Course(models.Model):
    CATEGORY_CHOICES = (
        ('math', 'Math'),
        ('science', 'Science'),
        ('language', 'Language'),
        ('tech', 'Technology'),
    )

    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='courses/photos/')
    instructor = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    num_students = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2)  # e.g. 1500.00
    num_hours = models.FloatField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    rate = models.FloatField(default=0)

    def __str__(self):
        return self.name
