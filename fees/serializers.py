from rest_framework import serializers
from .models import FeePlan

class FeePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeePlan
        fields = '__all__'