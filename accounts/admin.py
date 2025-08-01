from django.contrib import admin

# Register your models here.
from .models import User, Student, Teacher, Parent, Course


admin.site.register(User)
admin.site.register(Student)
admin.site.register(Teacher)