from django.urls import path
from . import views

urlpatterns = [
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/book/', views.appointment_book, name='appointment_book'),
    path('appointments/<int:pk>/approve/', views.appointment_approve, name='appointment_approve'),
    path('appointments/<int:pk>/reject/', views.appointment_reject, name='appointment_reject'),
]