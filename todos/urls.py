from django.urls import path
from .import views

urlpatterns = [
    path('todos/', views.todo_list, name='todo_list'),
    path('todos/add/', views.todo_add, name='todo_add'),
    path('todos/edit/<int:pk>/', views.todo_update, name='todo_update'),
    path('todos/delete/<int:pk>/', views.todo_delete, name='todo_delete'),
    path('todos/toggle/<int:pk>/', views.todo_toggle, name='todo_toggle'),
]