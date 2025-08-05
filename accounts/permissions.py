from rest_framework.permissions import BasePermission

class IsStudent(BasePermission):
    """
    Allows access only to users with user_type == 'student'.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'student'



from rest_framework import permissions

class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and
            hasattr(request.user, 'teacher_profile'))