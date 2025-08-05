from rest_framework.permissions import BasePermission

class IsStudent(BasePermission):
    """
    Allows access only to users with user_type == 'student'.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'student'



class IsTeacher(BasePermission):
    """
    Allows access only to users with user_type == 'teacher'.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'teacher'