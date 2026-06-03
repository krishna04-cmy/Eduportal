from django.urls import path
from . import views

urlpatterns = [
    path('ai_chat/', views.ai_chat_view, name='ai_chat'),
    path('ai_chat/send/', views.ai_chat_send, name='ai_chat_send'),
]