from django.contrib import admin
from .models import FeePlan, Order, Cart

admin.site.register(FeePlan)
admin.site.register(Order)
admin.site.register(Cart)