



from django.urls import path
from .views import CreateCourseView, ListCourseListView, UpdateCourseDetailView

urlpatterns = [
    # teacher
    path('create/courses/', CreateCourseView.as_view(), name='course-create'),
    # Any
    path('get/courses/', ListCourseListView.as_view(), name='course-list'),
    
    path('update/courses/<int:pk>/', UpdateCourseDetailView.as_view(), name='course-update'),
]
