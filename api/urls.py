from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('auth/login/', views.api_login, name='api_login'),
    path('auth/register/', views.api_register, name='api_register'),

    # Students
    path('students/', views.StudentListAPI.as_view(), name='api_students'),
    path('students/<int:pk>/', views.StudentDetailAPI.as_view(), name='api_student_detail'),

    # Attendance
    path('attendance/', views.AttendanceListAPI.as_view(), name='api_attendance'),

    # Results
    path('results/', views.ResultListAPI.as_view(), name='api_results'),

    # Todos
    path('todos/', views.TodoListAPI.as_view(), name='api_todos'),
    path('todos/<int:pk>/', views.TodoDetailAPI.as_view(), name='api_todo_detail'),

    # Blog
    path('posts/', views.PostListAPI.as_view(), name='api_posts'),
    path('posts/<int:pk>/', views.PostDetailAPI.as_view(), name='api_post_detail'),
]