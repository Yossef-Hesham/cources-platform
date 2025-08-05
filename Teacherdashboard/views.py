from django.shortcuts import render
from django.views import View
from .serializers import CourseSerializer
from rest_framework import generics, status
from accounts.models import Course
from accounts.permissions import IsTeacher  # Assuming you have this permission defined
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import serializers


class CreateCourseView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsTeacher]  # Assuming you have these permissions defined
    
    def validate(self, attrs):
        if self.request.user != attrs.get('instructor'):
            raise serializers.ValidationError("Only teachers can create courses.")
        # Custom validation logic can be added here if needed
        return super().validate(attrs)


class ListCourseListView(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsTeacher]
    
    def get_queryset(self):
        # Add select_related to optimize DB queries
        return Course.objects.filter(
            instructor=self.request.user.teacher_profile  # Assuming instructor links to Teacher model
        ).select_related('instructor__user')
    
    def get_serializer_context(self):
        # Pass request to serializer
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
class UpdateCourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    



