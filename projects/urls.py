from django.urls import path
from . import views

urlpatterns = [
    path('projects/', views.project_list, name='project_list'),
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('projects/<int:pk>/task/add/', views.task_add, name='task_add'),
    path('projects/<int:pk>/file/upload/', views.file_upload, name='file_upload'),
    path('projects/task/<int:pk>/complete/', views.task_complete, name='task_complete'),
    path('projects/<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('projects/<int:pk>/delete/', views.project_delete, name='project_delete'),
]
