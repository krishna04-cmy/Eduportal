from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

# DRF Router
router = DefaultRouter()
router.register('feeplans', views.FeePlanViewSet)

urlpatterns = [
    # Purane URLs — intact rakho
    path('fees/', views.fee_list, name='fee_list'),
    path('fees/cart/', views.cart_view, name='cart_view'),
    path('fees/cart/add/<int:pk>/', views.cart_add, name='cart_add'),
    path('fees/cart/remove/<int:pk>/', views.cart_remove, name='cart_remove'),
    path('fees/checkout/', views.checkout, name='checkout'),
    path('fees/orders/', views.order_list, name='order_list'),
    path('fees/all-orders/', views.all_orders, name='all_orders'),

    
    path('fees/add/', views.fee_plan_add, name='fee_plan_add'),
    path('fees/<int:pk>/edit/', views.fee_plan_edit, name='fee_plan_edit'),
    path('fees/<int:pk>/delete/', views.fee_plan_delete, name='fee_plan_delete'),

    # Naya DRF API URL
    path('api/', include(router.urls)),
]